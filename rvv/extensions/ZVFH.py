from rvv.extensions.extensions import RVVExtension

class ZVFH(RVVExtension):
    def add_extension(self):
        super().add_extension()
        self.rvv._valid_fsews.append(16)
    