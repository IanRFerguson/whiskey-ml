{% macro flavor_categories(field) %}
    CASE
        WHEN {{ field }} LIKE ANY(
            '%VANILLA%', '%CUSTARD%', '%HONEY%', 
            '%BUTTERSCOTCH%', '%SUGAR%', '%TOFFEE%', 
            '%CREAMY%', '%SWEET%', '%BUTTER%',
            '%CARAMEL%', '%MAPLE%', '%MARSHMALLOW%',
            '%MILK%', '%NOUGAT%') 
            THEN 'SWEET'
        WHEN {{ field }} LIKE ANY(
            '%ORANGE%', '%APPLE%', '%BANANA%', 
            '%BERRIES%', '%MANGO%', '%BERRY%'
            '%FRUIT%', '%LEMON%', '%FIGS%',
            '%CITRUS%') 
            THEN 'FRUITY'
        WHEN {{ field }} LIKE ANY(
            '%ALMOND%', '%WALNUT%', '%NUTTY%', 
            '%TOASTED%', '%ALMOND%', 
            '%COCONUT%', '%PECAN%')
            THEN 'NUTTY'
        WHEN {{ field }} LIKE ANY(
            '%PEPPER%', '%SPICY%', '%NUTMEG%', 
            '%CINNAMON%', '%CLOVE%', '%ALLSPICE%') 
            THEN 'SPICY'
        WHEN {{ field }} LIKE ANY(
            '%OAK%', '%LEATHER%', '%RANCIO%')
            THEN 'EARTHY'
        WHEN {{ field }} LIKE ANY(
            '%FLORAL%', '%BLACK TEA%') 
            THEN 'FLORAL'
        WHEN {{ field }} LIKE ANY(
            '%MELLOW%', '%SMOOTH%', '%RICH%', 
            '%UMAMI%', '%CHOCOLATE%')
            THEN 'RICH'
        WHEN {{ field }} LIKE ANY(
            '%CORN%', '%RYE%', '%BARLEY%') 
            THEN 'GRAIN'
        WHEN {{ field }} LIKE ANY(
            '%COCOA%', '%TOAST%', 
            '%PEPPER%', '%WARM%', '%MINT%') 
            THEN 'AROMATIC'
        ELSE 'UNCATEGORIZED'
    END
{% endmacro %}