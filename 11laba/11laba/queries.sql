-- 1. SELECT
SELECT * FROM books;

-- 2. WHERE
SELECT * FROM books WHERE category = 'Фантастика';

-- 3. ORDER BY
SELECT * FROM books ORDER BY year DESC;

-- 4. JOIN
SELECT readers.name, books.title
FROM loans
JOIN readers ON readers.id = loans.reader_id
JOIN books ON books.id = loans.book_id;

-- 5. LEFT JOIN
SELECT readers.name, loans.id
FROM readers
LEFT JOIN loans ON readers.id = loans.reader_id;

-- 6. GROUP BY
SELECT category, COUNT(*)
FROM books
GROUP BY category;

-- 7. HAVING
SELECT category, COUNT(*) AS amount
FROM books
GROUP BY category
HAVING COUNT(*) >= 2;

-- 8. COUNT
SELECT COUNT(*) AS books_count FROM books;

-- 9. AVG
SELECT AVG(year) AS average_year FROM books;

-- 10. INSERT
INSERT INTO readers(name, email)
VALUES ('Новый читатель', 'new_reader@example.com');

-- 11. UPDATE
UPDATE books
SET category = 'Классика'
WHERE id = 1;

-- 12. DELETE
DELETE FROM readers
WHERE id = 5;

-- 13. Подзапрос
SELECT * FROM books
WHERE year > (SELECT AVG(year) FROM books);

-- 14. Несколько условий
SELECT * FROM books
WHERE category = 'Фантастика' AND year >= 1960;

-- 15. Несколько связанных таблиц
SELECT readers.name, books.title, loans.loan_date
FROM loans
JOIN readers ON readers.id = loans.reader_id
JOIN books ON books.id = loans.book_id
WHERE loans.return_date IS NULL
ORDER BY loans.loan_date DESC;
