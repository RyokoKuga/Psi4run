# Psi4DnDrun_ ver.1.0.0
import os, sys, subprocess

try:
    # パス取得
    paths = sys.argv[1:]
    
    for path in paths:
        # ディレクトリの移動
        os.chdir(os.path.dirname(path))
        # Psi4の実行
        subprocess.run(["psi4", os.path.basename(path)])
except:
    pass