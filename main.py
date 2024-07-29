import re
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

def generate_links(app: Sphinx):
    # Chemin de base de la documentation HTML
    base_url = app.config.html_baseurl

    # Définir le pattern regex pour détecter :enerfox-linker:`module.module.class.function`
    pattern = re.compile(r':sphinx-doc-link:`(\w+(?:\.\w+)*)`')

    # Parcourir les fichiers sources (ajustez selon l'organisation de vos fichiers)
    for source_file in app.env.found_docs:
        # Charger le contenu du fichier source
        source_path = app.env.doc2path(source_file)
        with open(source_path, 'r') as file:
            content = file.read()

        # Rechercher tous les patterns correspondants
        matches = pattern.findall(content)

        # Pour chaque match, créer l'URL et remplacer dans le contenu
        for match in matches:
            components = match.split('.')
            module_path = '/'.join(components[:-1]) + '.html'
            anchor = components[-1]
            url = f"{base_url}/{module_path}#{'.'.join(components)}"
            link_format = f'<a href="{url}">{match}</a>'  # Format HTML pour le lien
            # Remplacer le pattern par l'URL dans le contenu
            content = content.replace(f":sphinx-doc-link:`{match}`", link_format)

        # Sauvegarder le contenu mis à jour
        with open(source_path, 'w') as file:
            file.write(content)

        logger.info(f"Updated links in {source_file}")

def setup(app: Sphinx):
    app.connect('builder-inited', generate_links)
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
