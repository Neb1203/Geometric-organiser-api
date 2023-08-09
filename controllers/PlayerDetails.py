import secrets
import json
from fastapi import FastAPI
from controllers.DBConnect import DBConnect
from controllers.hashSalt import hashSalt
class PlayerDetails:
    app = FastAPI()
    db_connect = DBConnect()
    def cloudLogin(self, email, password):
        qry = """
            SELECT JSON_OBJECT(
                'id', pd.id,
                'email', pd.email,
                'token', pd.token,
                'username', pd.userName,
                'password', pd.password,
                'settings_save', JSON_OBJECT(
                    'id', s.ID,
                    'music_volume', s.musicVolume,
                    'sfx_volume', s.sfxVolume
                ),
                'playerstatistics', JSON_OBJECT(
                    'id', p.ID,
                    'time_played', p.timePlayed,
                    'account_level', p.accountLevel,
                    'total_completed_lines', p.totalCompletedLines,
                    'rounds_played', p.roundsPlayed,
                    'campaign_attempts', p.campaignAttempts,
                    'campaign_completion_rate', p.campaignCompletionRate,
                    'average_round_length', p.averageRoundLength,
                    'high_score', p.highScore,
                    'deaths', p.deaths,
                    'average_score', p.averageScore
                )
            )
            FROM playerDetails pd
            LEFT JOIN settingsave s ON s.ID = pd._fk_settingsave
            LEFT JOIN playerstatistics p ON p.ID = pd._fk_player_statistics
            WHERE pd.email = %s AND pd.password = %s
            LIMIT 1
        """
        hashPassword = hashSalt(password)
        data = (email, hashPassword)
        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cursor.reset()

        return self.db_connect.cursor.fetchone()  # Fetch the first row

    def write(self, user_name, email, password):
        hexHash = hashSalt(password)
        token = secrets.token_urlsafe(48)

        qry = "INSERT INTO playerDetails (token, userName, password, email) VALUES (%s, %s, %s, %s)"
        data = (token, user_name, hexHash, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.reset()
