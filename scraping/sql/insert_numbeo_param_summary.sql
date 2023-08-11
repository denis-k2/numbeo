INSERT INTO
    numbeo_param (category_id, param)
VALUES ((SELECT category_id FROM numbeo_category WHERE category = 'Summary'), 'Family of four estimated monthly costs (without rent)');
INSERT INTO
    numbeo_param (category_id, param)
VALUES ((SELECT category_id FROM numbeo_category WHERE category = 'Summary'), 'A single person estimated monthly costs (without rent)');