"""DBhelper."""
import sqlite3


class DBHandler:
    """DBhelper."""

    def __init__(self):
        """Initialize the helper."""
        self.conn = sqlite3.connect("coins.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (id TEXT,
                                                             coins INTEGER)""")
        # self.dev()

    def dev(self):
        """Develop function, remove upon release."""
        self.cur.execute("INSERT INTO users (id, coins) VALUES (?,?)",
                         ("318810562081456128", 50))
        self.conn.commit()

    def getCoins(self, id):
        """Get a user's coins given their ID."""
        try:
            self.cur.execute("SELECT coins FROM users WHERE id = ?", [id])
            coins = self.cur.fetchone()
            return coins[0]
        except TypeError:
            # This exception is if the user doesn't exist in the database.
            self.addUser(id)
            # Return 0 coins
            return 0

    def addCoins(self, id, amount):
        """Calculate new coins after add."""
        currentCoins = self.getCoins(id)
        newCoins = currentCoins + amount
        self.setCoins(id, newCoins)

    def subtractCoins(self, id, amount):
        """Calculate new coins after subtract."""
        currentCoins = self.getCoins(id)
        newCoins = currentCoins - amount
        self.setCoins(id, newCoins)

    def setCoins(self, id, amount):
        """Edit coins."""
        self.cur.execute("UPDATE users SET coins = ? WHERE id = ?",
                         (amount, id))
        self.conn.commit()

    def addUser(self, id):
        """Add a user to the database."""
        self.cur.execute('INSERT INTO users(id,coins)VALUES(?,?)', (id, 50))
        self.conn.commit()
