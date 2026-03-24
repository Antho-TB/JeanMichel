# Guide pour automatiser l'arrêt de vos PostgreSQL

Étant donné qu'Azure impose un redémarrage tous les 7 jours pour un Flexible Server stoppé, nous avons préparé un script d'arrêt automatisé dans `scripts/Stop-Databases.ps1`.

Voici comment le déployer de manière sécurisée et pérenne directement sur le portail Azure :

### Étape 1 : Créer le compte Automation
1. Dans le portail Azure, cherchez et créez un **Compte Automation** (Automation Account).
2. Nom : `aa-tbgroupe-maintenance` (par exemple).
3. Option importante : Cochez l'activation de l'**Identité affectée par le système** (System Assigned Managed Identity). C'est ce qui permettra au script de se connecter sans mot de passe.

### Étape 2 : Donner les droits à cette identité
1. Allez sur votre Abonnement Azure (`shsv-prod` et les autres pertinents).
2. Dans **Contrôle d'accès (IAM)**, cliquez sur "Ajouter une attribution de rôle".
3. Choisissez le rôle **Contributeur** (ou équivalent).
4. Assignez-le à l'identité managée du compte Automation que vous venez de créer.

### Étape 3 : Créer et planifier le script (Runbook)
1. Dans le compte Automation, allez dans **Runbooks** > Créer un Runbook.
2. Nommez-le `Stop-PostgreSQL`.
3. Type : **PowerShell** (Version 7.2 ou 5.1).
4. Copiez-collez l'intégralité du code contenu dans le fichier `scripts/Stop-Databases.ps1` du projet `JeanMichel`.
5. Cliquez sur **Enregistrer** puis **Publier**.
6. Enfin, allez dans l'onglet **Planifications** de ce runbook, et créez une récurrence : **Tous les jours à minuit**.

De cette façon, même s'il est redémarré au bout de 7 jours, il s'éteindra automatiquement quelques heures plus tard.
