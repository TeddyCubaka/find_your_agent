class Utils:
    error = None

    def dataValidator(self, data: dict, valideKeys: list):
        missedKeys = []
        for key in valideKeys:
            if key not in data:
                missedKeys.append(key)
        self.error = {
            "missed_keys": ", ".join(missedKeys)
        }
        if len(missedKeys) > 0:
            return False
        return True

    def passwordVerify(self, pwd, pwd_repeat):
        if pwd != pwd_repeat:
            self.error = {
                "details": "les mots de passe saisie ne matchent pas"}
            return False
        if len(pwd) < 8:
            self.error = {
                "details": "le mot de passe doit avoir une taille supérieur ou égale à 8 caractère"}
