SOURCE_SPECIFICS = {
    'chefkoch.de': {
        'list-items': 'article.rsel-item',
        'list-item-header': 'h2.ds-heading-link::text',
        'list-item-url': 'a.rsel-recipe::attr("href")',
        'list-item-next': 'ul.ds-pagination li.ds-next a::attr("href")',

        'ingredients': 'table.ingredients tr',
        'ingredient-amount': 'td.td-left span::text',
        'ingredient-name': 'td.td-right span::text',
        'ingredient-name-secondary': 'td.td-right span a::text'
    }
}
