# (c) 2014-2020 Paul Sokolovsky. MIT license.
try:
    from uos import stat, remove
except:
    from os import stat, remove
from . import source
import json


class Loader(source.Loader):

    def load(self, name):
        o_path = self.pkg_path + self.compiled_path(name)
        try:
            o_stat = stat(o_path)
            deps_path = self.input_filename(name) + ".deps"
            with open(deps_path, "r") as f:
                deps = json.load(f)
                
            for dep in deps:
                i_path = self.input_filename(dep)
                i_stat = stat(i_path)
                if i_stat[8] > o_stat[8]:
                # dependency file is newer, remove output to force recompile
                    remove(o_path)
                    break
        except Exception as e:
            print(f"failed to check dependencies, forcing rebuild: {e}")
            remove(o_path)
        finally:
            return super().load(name)
