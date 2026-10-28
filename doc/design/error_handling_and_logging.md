# 例外処理・ログ設計

## 1. 目的

SAPIClip は PyInstaller の `--noconsole` オプションを使用して配布用 EXE を作成する。
そのため、標準出力や標準エラー出力だけでは、利用環境で発生した問題を追跡できない。

本設計では、次の情報をファイルへ記録する。

- アプリケーションの起動と正常終了
- アプリケーション実行中に伝播した例外
- クリップボード監視スレッドの開始、正常停止、例外
- Tkinter コールバック内で発生した未処理例外

例外発生時は、技術的な詳細をログへ記録し、利用者には簡潔なエラーダイアログを表示する。

## 2. 関連ファイル

| ファイル | 役割 |
| --- | --- |
| [`src/app_logging.py`](../../src/app_logging.py) | ログの保存先、形式、ローテーション、ロガー階層を設定する |
| [`src/application.py`](../../src/application.py) | ログを初期化し、アプリケーションの起動・終了と、実行中に伝播した例外を記録する |
| [`src/main_window.py`](../../src/main_window.py) | 監視スレッドと Tkinter コールバックのログ・例外処理を行う |

ログ設定は `application.py` から起動時に一度だけ初期化する。各モジュールはハンドラーを個別に追加せず、`get_logger()` で子ロガーを取得する。

## 3. ログファイル

### 3.1 保存先

配布用 EXE では、`SAPIClip.exe` と同じフォルダに `logs` フォルダを作成する。

```text
SAPIClip.exe
logs/
└── SAPIClip.log
```

| 実行方法 | 保存先の基準 |
| --- | --- |
| PyInstaller で作成した EXE | `sys.executable` が存在するフォルダ |
| Python ソースから実行 | プロジェクトのルートフォルダ |

PyInstaller の `sys._MEIPASS` は一時展開先であるため、ログの保存先には使用しない。

### 3.2 ローテーション

`RotatingFileHandler` を使用し、ログファイルが無制限に増えないようにする。

| 項目 | 設定値 |
| --- | --- |
| 文字コード | UTF-8 |
| 1ファイルの最大サイズ | 1 MiB（1,048,576バイト） |
| バックアップ数 | 3世代 |
| 現在のログ | `SAPIClip.log` |
| 過去のログ | `SAPIClip.log.1` ～ `SAPIClip.log.3` |

ログフォルダまたはログファイルを作成できない場合、`setup_logging()` は `None` を返す。ログの初期化失敗だけを理由にアプリケーションを停止させない。

### 3.3 出力形式

```text
日時 ログレベル [ロガー名] [スレッド名] メッセージ
```

例：

```text
2026-10-28 11:50:59,526 INFO [SAPIClip.application] [MainThread] SAPIClip 0.2.0 started
2026-10-28 11:51:04,612 INFO [SAPIClip.application] [MainThread] SAPIClip 0.2.0 stopped normally
```

## 4. ロガー階層

アプリケーション共通の親ロガーを `SAPIClip` とし、モジュールごとに子ロガーを使用する。

```text
SAPIClip
├── SAPIClip.application
└── SAPIClip.main_window
```

使用例：

```python
from app_logging import get_logger

logger = get_logger(__name__)
```

Python 標準の `logging` はスレッドセーフであるため、メインスレッドと監視スレッドから同じログファイルへ記録できる。

## 5. 例外処理の経路

| 発生場所 | 捕捉方法 | ログ | 利用者への通知 |
| --- | --- | --- | --- |
| アプリケーション実行中 | `application.py` の `try` / `except` | `logger.exception()` でトレースバックを記録 | Windows の `MessageBoxW` |
| クリップボード監視スレッド | `monitor_clipboard()` の `try` / `except` | `logger.exception()` でトレースバックを記録 | キュー経由でメインスレッドがダイアログを表示 |
| Tkinter コールバック | `root.report_callback_exception` | `logger.error(..., exc_info=...)` でトレースバックを記録 | Tkinter の `messagebox.showerror()` |

### 5.1 アプリケーションの起動と終了

`application.py` は、ログ初期化後に起動ログを記録してから `Application.start()` を呼び出す。

- `Application.start()` が正常に戻った場合は、`else` 節で正常終了を記録する。
- 例外が伝播した場合は、`except` 節でトレースバックを記録し、エラーダイアログを表示する。
- エラーダイアログの表示後は、終了コード `1` でアプリケーションを終了する。
- 例外終了を正常終了として記録しないため、終了ログは `finally` ではなく `else` で記録する。

正常終了の例：

```text
INFO [SAPIClip.application] [MainThread] SAPIClip 0.2.0 started
INFO [SAPIClip.application] [MainThread] SAPIClip 0.2.0 stopped normally
```

### 5.2 クリップボード監視スレッド

監視スレッドには `ClipboardMonitor` という名前を設定する。

- スレッド開始時に `Clipboard monitoring started` を記録する。
- 停止ボタンやアプリ終了によって正常に監視ループを抜けた場合、`else` 節で `Clipboard monitoring stopped normally` を記録する。
- 例外が発生した場合、`except` 節で `Clipboard monitoring failed` とトレースバックを記録する。
- `finally` 節では、成否にかかわらずメインスレッドへ終了通知を送る。

監視スレッドで例外が発生しても、アプリケーション本体が正常な手順で終了した場合は、最後にアプリケーションの正常終了ログが記録される。これは「監視処理は失敗したが、アプリケーション自体は正常に終了処理を行った」という意味である。

### 5.3 Tkinter コールバック

Tkinter は、ボタン操作や `after()` から呼ばれたコールバックの例外を内部で捕捉する。そのため、`Application.start()` の外側にある `try` / `except` には伝播しない。

`MainWindow` の生成時に、次のハンドラーを設定する。

```python
self.root.report_callback_exception = self.handle_tk_exception
```

`handle_tk_exception()` は、Tkinter から渡された例外型、例外値、トレースバックをログへ記録し、利用者へエラーダイアログを表示する。例外を処理した後も、Tkinter のイベントループは継続する。

## 6. ログレベル

| レベル | 用途 |
| --- | --- |
| `INFO` | アプリケーションや監視スレッドの開始・正常終了 |
| `WARNING` | 処理を継続できるが、利用者が確認すべき状態（将来利用） |
| `ERROR` | アプリケーション実行中、監視スレッド、Tkinter コールバックの例外 |
| `DEBUG` | 詳細な調査情報（既定の `INFO` 設定では出力しない） |

例外の `except` 節では `logger.exception()` を使用する。Tkinter から例外情報を引数として受け取る場合は、`exc_info=(exc_type, exc_value, tb)` を指定する。

## 7. プライバシーとセキュリティ

クリップボードには個人情報や認証情報が含まれる可能性がある。次の情報はログへ記録しない。

- クリップボードの内容
- 読み上げた文章
- 置換前後の文章
- `settings.json` の内容

例外メッセージには、環境によってファイルパスなどが含まれる可能性がある。ログを GitHub の Issue などへ添付する場合は、利用者が内容を確認してから共有する。

実行時に作られる `*.log` と `dist/` は `.gitignore` の対象であり、リポジトリへコミットしない。

## 8. 制限事項

次の場合、正常終了ログは記録されない。

- タスクマネージャーによる強制終了
- Windows Sandbox や OS の強制終了
- 電源断
- Python プロセス自体のクラッシュ

起動ログがあり、対応する正常終了ログがない場合は、強制終了または異常終了の可能性を調査する。

また、次の例外は現時点で個別のログ対象外である。

- DPI 設定時に無視している例外
- 自動言語判定で読み上げ音声を選択できなかった場合の例外
- `Exception` を経由しない `SystemExit` や `KeyboardInterrupt`

## 9. 動作確認

### 9.1 正常起動・正常終了

1. アプリケーションを起動する。
2. 通常の方法でウィンドウを閉じる。
3. 起動ログと `stopped normally` が記録されることを確認する。

### 9.2 起動時例外

Windows Sandbox など、SAPI の初期化に失敗する環境で確認する。

1. 起動失敗のダイアログが表示されることを確認する。
2. `Application failed` と完全なトレースバックが記録されることを確認する。
3. `stopped normally` が記録されないことを確認する。
4. プロセスの終了コードが `1` であることを確認する。

### 9.3 監視スレッド

1. 開始ボタンを押し、`Clipboard monitoring started` が記録されることを確認する。
2. 停止ボタンを押し、`Clipboard monitoring stopped normally` が記録されることを確認する。
3. 監視処理内で例外が発生した場合、エラーダイアログとトレースバックが記録されることを確認する。

### 9.4 Tkinter コールバック

テスト時のみ、`mainloop()` 開始後に `after()` でテスト用例外を発生させる。

```python
self.root.after(1000, self.raise_test_exception)
```

```python
def raise_test_exception(self):
    raise RuntimeError("Tkinter exception handler test")
```

次の項目を確認する。

- エラーダイアログが表示される。
- `Unhandled Tkinter callback exception` とトレースバックが記録される。
- ダイアログを閉じた後もアプリケーションが動作する。
- 通常の方法で終了すると `stopped normally` が記録される。

確認後は、テスト用の `after()` と `raise_test_exception()` を必ず削除する。

## 10. 保守時の注意

- 新しいモジュールからログを出力する場合は、`get_logger()` で子ロガーを取得する。
- 各モジュールで `setup_logging()` やハンドラーの追加を行わない。
- 新しいスレッドを追加する場合は、識別しやすいスレッド名と例外処理を設定する。
- ログへ利用者の入力内容を追加する場合は、必要性と個人情報への影響を確認する。
- 例外を単に握りつぶさず、想定内の例外か、ログへ記録すべき障害かを判断する。
