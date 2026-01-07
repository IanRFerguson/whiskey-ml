{% macro flavor_categories(field) %}
    CASE
        WHEN {{ field }} LIKE ANY(
            '%VANILLA%', '%CUSTARD%', '%HONEY%', 
            '%BUTTERSCOTCH%', '%SUGAR%', '%TOFFEE%', 
            '%CREAMY%', '%SWEET%', '%BUTTER%',
            '%CARAMEL%', '%MAPLE%', '%MARSHMALLOW%',
            '%MILK%', '%NOUGAT%', '%CAKE%',
            '%BUTTERY VANILLA%', '%BROWN SUGAR%', '%WHITE CHOCOLATE%') 
            THEN 'SWEET'
        WHEN {{ field }} LIKE ANY(
            '%ORANGE%', '%APPLE%', '%BANANA%', 
            '%BERRIES%', '%MANGO%', '%BERRY%',
            '%FRUIT%', '%LEMON%', '%FIGS%',
            '%CITRUS%', '%CHERRY%', '%STONE FRUIT%',
            '%RAISIN%', '%PEACH%', '%APRICOT%',
            '%RED BERRIES%', '%TROPICAL FRUITS%', '%TROPICAL FRUIT%',
            '%PEAR%', '%RASPBERRY%', '%DRIED FRUITS%',
            '%DRIED FRUIT%', '%GREEN APPLE%', '%RED APPLE%') 
            THEN 'FRUITY'
        WHEN {{ field }} LIKE ANY(
            '%ALMOND%', '%WALNUT%', '%NUTTY%', 
            '%TOASTED%', '%COCONUT%', '%PECAN%',
            '%ALMONDS%', '%WALNUTS%', '%NUTS%', 
            '%HAZELNUTS%')
            THEN 'NUTTY'
        WHEN {{ field }} LIKE ANY(
            '%PEPPER%', '%SPICY%', '%NUTMEG%', 
            '%CINNAMON%', '%CLOVE%', '%ALLSPICE%',
            '%GINGER%', '%ANISE%', '%CANDIED GINGER%') 
            THEN 'SPICY'
        WHEN {{ field }} LIKE ANY(
            '%OAK%', '%LEATHER%', '%RANCIO%',
            '%TOASTED OAK%', '%GRASSY%')
            THEN 'EARTHY'
        WHEN {{ field }} LIKE ANY(
            '%FLORAL%', '%BLACK TEA%', '%ROSE%') 
            THEN 'FLORAL'
        WHEN {{ field }} LIKE ANY(
            '%MELLOW%', '%SMOOTH%', '%RICH%', 
            '%UMAMI%', '%CHOCOLATE%', '%DARK CHOCOLATE%',
            '%MILK CHOCOLATE%', '%SAVOURY%')
            THEN 'RICH'
        WHEN {{ field }} LIKE ANY(
            '%CORN%', '%RYE%', '%BARLEY%',
            '%MALTED BARLEY%', '%MALT%', '%BREAD%') 
            THEN 'GRAIN'
        WHEN {{ field }} LIKE ANY(
            '%COCOA%', '%TOAST%', '%WARM%', 
            '%MINT%', '%HERBAL%', '%FRESH%') 
            THEN 'AROMATIC'
        WHEN {{ field }} LIKE ANY(
            '%SMOKY%', '%PEATY%')
            THEN 'SMOKY'
        ELSE 'UNCATEGORIZED'
    END
{% endmacro %}