"""
pydantic v1とv2の互換性を解決するためのパッチモジュール
"""

import sys
import types
import inspect
from functools import wraps

# エラーデータクラスを直接定義
class ErrorData:
    """MCPエラーデータ用の互換クラス"""
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

# パッチ適用関数
def apply_pydantic_patches():
    """pydanticのBaseModelにパッチを適用する"""
    try:
        import pydantic
        from pydantic import BaseModel
        from pydantic.version import VERSION as PYDANTIC_VERSION
        
        print(f"Detected pydantic version: {PYDANTIC_VERSION}")
        
        if PYDANTIC_VERSION.startswith('2'):
            # 既にパッチが適用されているかチェック
            if hasattr(BaseModel, '_mcp_patched'):
                print("Patches already applied, skipping...")
                return True
            # mcp.types.ErrorDataクラスをモンキーパッチ
            try:
                from mcp.types import ErrorData as MCPErrorData
                # オリジナルのクラスを保存
                original_error_data = MCPErrorData
                
                # ErrorDataクラスを置き換え
                sys.modules['mcp.types'].ErrorData = ErrorData
                print("Replaced mcp.types.ErrorData with compatibility class")
            except (ImportError, AttributeError) as e:
                print(f"Could not patch ErrorData: {e}")
            
            # BaseModelの__new__メソッドをパッチ
            original_new = BaseModel.__new__
            
            @wraps(original_new)
            def patched_new(cls, *args, **kwargs):
                # 引数の数をチェック
                if len(args) > 1:
                    print(f"Intercepted BaseModel.__new__ with {len(args)} args")
                    # 最初の引数（クラス）だけを保持
                    return object.__new__(cls)
                try:
                    return original_new(cls, *args, **kwargs)
                except TypeError:
                    # エラーが発生した場合はシンプルに作成
                    return object.__new__(cls)
            BaseModel.__new__ = patched_new
            
            # BaseModelの__init__メソッドをパッチ
            original_init = BaseModel.__init__
            
            @wraps(original_init)
            def patched_init(self, *args, **kwargs):
                # 引数の数をチェック
                if len(args) > 0:
                    print(f"Intercepted BaseModel.__init__ with {len(args)} args: {args}")
                    # 位置引数が辞書形式の場合、キーワード引数として展開
                    if len(args) == 1 and isinstance(args[0], dict):
                        kwargs.update(args[0])
                        return original_init(self, **kwargs)
                    elif len(args) > 1:
                        # 複数の位置引数がある場合は、最初の引数だけを使用
                        if isinstance(args[0], dict):
                            kwargs.update(args[0])
                        return original_init(self, **kwargs)
                    # その他の場合は位置引数を無視
                    return original_init(self, **kwargs)
                return original_init(self, *args, **kwargs)
            
            BaseModel.__init__ = patched_init
            
            # パッチ適用マークを設定
            BaseModel._mcp_patched = True
            
            print("Pydantic v2 patched for compatibility with v1 code")
            return True
    except ImportError:
        print("Pydantic not found, no patching needed")
    except Exception as e:
        print(f"Failed to patch pydantic: {e}")
    
    return False

# モジュールがインポートされたときにパッチを適用
patched = apply_pydantic_patches()

# モジュールの公開インターフェース
__all__ = ['patched', 'ErrorData', 'apply_pydantic_patches']
