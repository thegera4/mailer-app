instructions = [
    "DROP TABLE IF EXISTS email;",
    """
        CREATE TABLE email (
            id INT PRIMARY KEY AUTO_INCREMENT,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL
        );
    """,
    """
        INSERT INTO email (email, subject, content)
        VALUES ('test@email.com','Hello this is a test','This is the content of the test email'),
        ('anothertest@email.com','Hello this is another test','This is the content of another test email');
    """
]
