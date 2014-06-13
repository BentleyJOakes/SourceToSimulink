import sys
import os

class BlockCreator():

    @staticmethod
    def load_block(block_type):
        node_kind = block_type.split(".")[-1]
        cl = BlockCreator.load_class("blocks." + node_kind + ".py")
        return cl

    @staticmethod
    # function to dynamically load a new class
    def load_class(full_class_string):
        directory, module_name = os.path.split(full_class_string)
        module_name = os.path.splitext(module_name)[0]

        path = list(sys.path)
        sys.path.insert(0, directory)
        module = None

        try:
            module = __import__(module_name)
        except ImportError:
            print("Couldn't find " + module_name)
            return BlockCreator.get_basic_block()
        finally:
            sys.path[:] = path  # restore
            module_name = module_name.split(".")[-1]
        mod = getattr(module, module_name)

        try:
            cl = getattr(mod, module_name)
            return cl
        except Exception:
            print("Couldn't find " + module_name)
            return BlockCreator.get_basic_block()


    @staticmethod
    def get_basic_block():
        module = __import__("blocks.Block")
        mod = getattr(module, "Block")
        return getattr(mod, "Block")