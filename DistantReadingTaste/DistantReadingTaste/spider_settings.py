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
    },
    
    'kochbar.de': {
        'list-items': 'div.kb-teaser-list-item',
        'list-item-header': 'span.kb-teaser-list-link::text',
        'list-item-url': 'div.kb-teaser-list-item-wrapper::attr("data-url")',
        'list-item-next': 'div.kb-pagination-container ul li span.masked-url::attr("data-url")',

        'ingredients': 'table.ks-ingredients-table tr',
        'ingredient-amount': 'td span.ks-ingredients-table__amount::text',
        'ingredient-name': 'td::text',
        'ingredient-name-secondary': 'span a::text'

    },
    
    'daskochrezept.de': {
        'list-items': 'li.list-group__item ',
        'list-item-header': 'div.teaser-search-result teaser-search-result--recipe a.teaser-search-result__title::text',
        'list-item-url': 'a.teaser-search-result__title::attr("href")',
        'list-item-next': 'a.pager-item__inner::attr("href")',
        
        'ingredients': 'div.ingredients-list ingredients-list--two-columns',
        'ingredient-amount': 'span.ingredients-list__amount span.data-ingredient-value::text',
        'ingredient-name': 'span.ingredients-list__name a::text',
        'ingredient-name-secondary': ''
    },
    
    'oetker.de': {
        'list-items': 'div.m068-recipeteaser',
        'list-item-header': 'div.m068-recipeteaser-info a span.e001-link-text::text',
        'list-item-url': 'div.m068-recipeteaser-info a::attr("href")',
        'list-item-next': '', 
        
        'ingredients': 'table.m053-ingredients-table tbody tr.ingredients',
        'ingredient-amount': 'td.m053-ingredients-table-value::text',
        'ingredient-name': 'td.m053-ingredients-table-name::text',
        'ingredient-name-secondary': ''
    },
    
    'gutekueche.at': {
        'list-items': 'div.col div.linkarea griditem-list-teaser div.grid div.col col-2-3 col-xs-2-2',
        'list-item-header': 'h3 a::text',
        'list-item-url': 'h3 a::attr("href")',
        'list-item-next': 'div.paging ul li a::attr("href")',
        
        'ingredients': 'div.ingredients-table table.striped tbody tr',
        'ingredient-amount': 'th::text',
        'ingredient-name': 'td.text-right::text',
        'ingredient-name-secondary': ''
    },
    
    'kochrezepte.at': {
        'list-items': 'div.recipe_list_entry box clearfix',
        'list-item-header': 'div.desc_box div.main a::text',
        'list-item-url': 'div.desc_box div.main a::attr("href")',
        'list-item-next': 'div.col-xs-12 div.pull-left div.pagination li.active a::attr("href")',
        
        'ingredients': 'table.table table-striped table-hover table-condensed',
        'ingredient-amount': 'tr td::text',
        'ingredient-name': 'tr td::text',
        'ingredient-name-secondary': ''
    },
    
    'issgesund.at': {
        'list-items': 'div.col-sm-4 px-2',
        'list-item-header': 'a div.card mb-4 shadow-sm hoverable div.card-image lazy applied h2.card-title a::text',
        'list-item-url': 'a::attr("href")',
        'list-item-next': '', 
        
        'ingredients': 'div.col-sm-6 ul.collection with-header',
        'ingredient-amount': 'li.collection-item span.ingredient-amount::text',
        'ingredient-name': 'li.collection-item::text',
        'ingredient-name-secondary': ''
    },
    
    'steiermark.com': {
        'list-items': 'div.col col-sm-4 section.teaser category-teaser row--same-height__item bg-grey',
        'list-item-header': 'div.class="teaser__head__text text-shadow text-white text-center h3.no-hl-style a::text',
        'list-item-url': 'div.class="teaser__head__text text-shadow text-white text-center h3.no-hl-style a::attr("href")',
        'list-item-next': 'ul.pagination nav nav-tabs js-filter-form-paging  li a::attr("href")', 
        
        'ingredients': 'div.col-sm-4 ul.list-unstyled list-primary list-labels fz20',
        'ingredient-amount': 'li div.bg-green d-ib list-labels__label::text',
        'ingredient-name': 'li div.bg-green d-ib list-labels__label::text',
        'ingredient-name-secondary': ''
    },
    
    'gutekueche.ch': {
        'list-items': 'section.sec article.grid teaser-card linkarea',
        'list-item-header': 'div.col col-2-3 col-s-2-3 col-xs-2-2 h3 a::text',
        'list-item-url': 'div.col col-2-3 col-s-2-3 col-xs-2-2 h3 a::attr("href")',
        'list-item-next': 'div.paging ul li a::attr("href")',
        
        'ingredients': 'div.grid sec div.col col-2-3 recipe-ingredients table tbody tr.ingredients',
        'ingredient-amount': 'td.text-right::text',
        'ingredient-name': 'th a::text',
        'ingredient-name-secondary': ''
    },
    
    'migusto.migros.ch': {
        'list-items': 'article.c-article-teaser--recipe div.c-teaser--recipe is-four div.teaser__content-wrapper',
        'list-item-header': 'div.teaser__headline span::text',
        'list-item-url': '',
        'list-item-next': '',
        
        'ingredients': 'div.c-recipe-ingredients ul.recipe-ingredients__recipe-list is-active li.recipe-ingredients__item',
        'ingredient-amount': 'span.recipe-ingredients__value::text',
        'ingredient-name': 'span.recipe-ingredients__label::text',
        'ingredient-name-secondary': ''
    },
    
    'fooby.ch': {
        'list-items': 'div.teaser__click-area',
        'list-item-header': 'div.teaser__inner div.teaser__body div.teaser__body-title::text',
        'list-item-url': 'a::attr("href")',
        'list-item-next': '',
        
        'ingredients': 'div.h-hide-medium-up div.t5-recipe__ingredient-overview div.recipe-ingredientlist__step-wrapper div.recipe-ingredientlist__ingredient-wrapper',
        'ingredient-amount': 'span.recipe-ingredientlist__ingredient-quantity span.data-portion-calculator-initial-quantity::text',
        'ingredient-name': 'span.recipe-ingredientlist__ingredient-desc::text',
        'ingredient-name-secondary': ''
    }
}
