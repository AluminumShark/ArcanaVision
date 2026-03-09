"""ArcanaVision 統一啟動入口 — 同時啟動 FastAPI 後端 + Vite 前端 dev server。"""

import subprocess
import sys
import time
import signal
import os

API_PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")


def main() -> None:
    procs: list[subprocess.Popen] = []

    def cleanup(sig=None, frame=None):
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        for p in procs:
            try:
                p.wait(timeout=5)
            except Exception:
                p.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print()
    print("  ✦ ArcanaVision — 統一啟動 ✦")
    print()

    # 1. FastAPI 後端
    print(f"  [Backend]  啟動 FastAPI on http://0.0.0.0:{API_PORT}")
    api_proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "api.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(API_PORT),
            "--reload",
        ],
        cwd=os.path.dirname(__file__) or ".",
    )
    procs.append(api_proc)

    time.sleep(1)

    # 2. Vite 前端 dev server
    print("  [Frontend] 啟動 Vite dev server on http://localhost:5173")
    web_proc = subprocess.Popen(
        ["pnpm", "dev"],
        cwd=WEB_DIR,
        shell=True,
    )
    procs.append(web_proc)

    print()
    print("  ─────────────────────────────────────────")
    print("  前端：http://localhost:5173")
    print(f"  後端：http://localhost:{API_PORT}")
    print(f"  API：http://localhost:{API_PORT}/api/spreads")
    print("  ─────────────────────────────────────────")
    print("  Ctrl+C 停止所有服務")
    print()

    try:
        while True:
            for p in procs:
                ret = p.poll()
                if ret is not None:
                    print(f"  ⚠ 子程序 PID {p.pid} 已結束 (code={ret})")
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
