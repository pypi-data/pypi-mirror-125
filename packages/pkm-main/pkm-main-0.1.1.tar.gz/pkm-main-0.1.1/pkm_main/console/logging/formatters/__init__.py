from .builder_formatter import BuilderLogFormatter


FORMATTERS = {
    "pkm_buildsys.masonry.builders.builder": BuilderLogFormatter(),
    "pkm_buildsys.masonry.builders.sdist": BuilderLogFormatter(),
    "pkm_buildsys.masonry.builders.wheel": BuilderLogFormatter(),
}
