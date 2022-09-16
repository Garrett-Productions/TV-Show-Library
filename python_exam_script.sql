-- INSERT INTO python_exam.shows (id, user_id, title, network, release_date, creator, description)
-- VALUES (3, 3, 'Spongebob', 'Nickolodean', '2022-08-18', 'Cole', 'An awesome Cartoon');

-- SELECT * FROM python_exam.users;

-- SELECT * FROM shows JOIN users on shows.user_id = users.id;
-- SELECT * FROM python_exam.shows;
SELECT shows.id AS id, shows.user_id AS user_id, shows.title AS title, shows.network AS network, shows.release_date AS release_date, shows.description AS description, shows.created_at AS created_at, shows.updated_at AS updated_at, users.first_name AS creator FROM shows JOIN shows.users ON users.id = shows.user_id;SELECT * FROM shows JOIN users on shows.user_id = users.id WHERE shows.id = 1;

SELECT * FROM shows JOIN users on shows.user_id WHERE user_id = users.id;

SELECT * FROM users;
SELECT * FROM shows;

