INSERT INTO
    numbeo_params (category_id, params)
VALUES ((SELECT category_id FROM numbeo_categories WHERE category = 'Summary'), 'Family of four estimated monthly costs (without rent)');
INSERT INTO
    numbeo_params (category_id, params)
VALUES ((SELECT category_id FROM numbeo_categories WHERE category = 'Summary'), 'A single person estimated monthly costs (without rent)');