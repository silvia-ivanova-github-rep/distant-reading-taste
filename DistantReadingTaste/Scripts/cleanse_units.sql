# english
UPDATE recipe_ingredients SET unit='Ounce' WHERE unit IN ('ounces', 'ounce');
UPDATE recipe_ingredients SET unit='Gram' WHERE unit IN ('grams', 'gram');
UPDATE recipe_ingredients SET unit='Pound' WHERE unit IN ('pound', 'pounds');
UPDATE recipe_ingredients SET unit='Kilogram' WHERE unit IN ('kilogram', 'kilograms');
UPDATE recipe_ingredients SET unit='Pinch' WHERE unit IN ('pinch', 'pinches', 'dash', 'dashes', 'splash');
UPDATE recipe_ingredients SET unit='Liter' WHERE unit IN ('liter', 'liters');
UPDATE recipe_ingredients SET unit='Fluid ounce' WHERE unit IN ('fluid ounces', 'fluid ounce');
UPDATE recipe_ingredients SET unit='Gallon' WHERE unit IN ('gallon', 'gallons');
UPDATE recipe_ingredients SET unit='Pint' WHERE unit IN ('pint', 'pints');
UPDATE recipe_ingredients SET unit='Quart' WHERE unit IN ('quart', 'quarts');
UPDATE recipe_ingredients SET unit='Milliliter' WHERE unit IN ('milliliter', 'milliliters');
UPDATE recipe_ingredients SET unit='Drop' WHERE unit IN ('drop', 'drops');
UPDATE recipe_ingredients SET unit='Cup' WHERE unit IN ('cup', 'cups');
UPDATE recipe_ingredients SET unit='Tablespoon' WHERE unit IN ('tablespoon', 'tablespoons');
UPDATE recipe_ingredients SET unit='Teaspoon' WHERE unit IN ('teaspoon', 'teaspoons', 't', 't.');
UPDATE recipe_ingredients SET unit='Clove' WHERE unit IN ('clove', 'cloves');

# german
UPDATE recipe_ingredients SET unit='Tablespoon' WHERE unit IN ('EL', 'EL, gestr.', 'EL, gehäuft');
UPDATE recipe_ingredients SET unit='Teaspoon' WHERE unit IN ('TL', 'TL, gehäuft', 'TL, gestr.');
UPDATE recipe_ingredients SET unit='Milliliter' WHERE unit IN ('ml');
UPDATE recipe_ingredients SET unit='Milligram' WHERE unit IN ('mg');
UPDATE recipe_ingredients SET unit='Kilogram' WHERE unit IN ('kg');
UPDATE recipe_ingredients SET unit='Gram' WHERE unit IN ('g');
UPDATE recipe_ingredients SET unit='Cup' WHERE unit IN ('Tasse/n', 'Tasse');
UPDATE recipe_ingredients SET unit='Pinch' WHERE unit IN ('etwas', 'Schuss', 'n. B.', 'Prise', 'wenig', 'Msp.', 'Prisen');
UPDATE recipe_ingredients SET unit='Drop' WHERE unit IN ('Tropfen');
UPDATE recipe_ingredients SET unit='Dash' WHERE unit IN ('Spritzer');
UPDATE recipe_ingredients SET unit='Liter' WHERE unit IN ('Liter');
UPDATE recipe_ingredients SET unit='Clove' WHERE unit IN ('Zehe/n');
UPDATE recipe_ingredients SET unit='Serving' WHERE unit IN ('Port.');
UPDATE recipe_ingredients SET unit='Handful' WHERE unit IN ('kl. Bund');
UPDATE recipe_ingredients SET unit='Bunch' WHERE unit IN ('Bund', 'Bündel', 'Topf');
UPDATE recipe_ingredients SET unit='Can' WHERE unit IN ('Dose/n', 'Dose', 'Glas', 'kl. Gläser', 'kl. Glas', 'gr. Dose/n', 'Gläser', 'kl. Dose/n');
UPDATE recipe_ingredients SET unit='Cup' WHERE unit IN ('Becher', 'Tube/n');
UPDATE recipe_ingredients SET unit='Carton' WHERE unit IN ('Kästchen', 'Schälchen', 'Pkt.', 'Pck.', 'Paket');
UPDATE recipe_ingredients SET unit='Bottle' WHERE unit IN ('gr. Flasche', 'Flasche', 'Flaschen', 'kl. Flasche/n', 'gr. Glas');
UPDATE recipe_ingredients SET unit='Bag' WHERE unit IN ('Beutel', 'Tüte/n');
UPDATE recipe_ingredients SET unit='' WHERE unit IN ('große', 'großer', 'Scheibe/n', 'Körner', 'm.-große', 'einige', 'Stiel/e', 'Stiele', 'Blätter', 'Stängel', 'kl. Stück',
                                                     'Kopf', 'einige Stiele', 'Knolle/n', 'Blatt', 'großes', 'Paar', 'kleiner', 'halbe', 'm.-großer', 'Rolle', 'Köpfe',
                                                     'dünne', 'Kugel/n', 'Teil/e', 'Ring/e', 'Wurzel', 'kleines', 'Platte/n', 'Wurzel/n', 'Kugeln', 'großen', 'Staude', 'extra',
                                                     'mehr', 'kl. Scheibe', 'Rippe/n', 'Zweig/e', 'Ecke', 'Beet/e', 'gr. Scheibe', 'gr. Kopf', 'kl. Kopf', 'Tafel',
                                                     'Stange/n', 'Stück', 'Streifen', 'Handvoll', 'evtl.', 'cm', 'kleine', 'Würfel', 'viel', 'Kugel', 'm.-großes', 'dicke');