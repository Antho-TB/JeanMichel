<#
.SYNOPSIS
    Migre une Azure Function d'un plan Premium vers un plan Consumption (Y1).
    ATTENTION : Cela supprime la Function App actuelle pour la recréer. Le code source devra être redéployé via CI/CD.
#>

$AppName = "func-shsv-veille-prod"
$ResourceGroup = "rg-shsv-veille-prod"
$OldPlanName = "plan-shsv-veille-prod"
$StorageAccount = "stshsvveilleprod"
$Subscription = "cef4660c-cb19-43f7-b3f3-c6575a4f836a"

Write-Output "Sélection de l'abonnement..."
az account set --subscription $Subscription

Write-Output "Sauvegarde des paramètres de configuration actuels dans settings_backup.json..."
az functionapp config appsettings list -n $AppName -g $ResourceGroup > settings_backup.json

Write-Output "Suppression de la Function App (Destructif) !"
az functionapp delete -n $AppName -g $ResourceGroup

Write-Output "Suppression de l'ancien plan Premium ($OldPlanName)..."
az appservice plan delete -n $OldPlanName -g $ResourceGroup --yes

Write-Output "Création de la nouvelle Function App en plan Consommation (Y1)..."
az functionapp create --name $AppName --storage-account $StorageAccount --consumption-plan-location northeurope --resource-group $ResourceGroup --os-type Linux --runtime python --runtime-version 3.11 --functions-version 4

Write-Output "Migration terminée ! Vous devez maintenant : "
Write-Output "1. Rétablir les variables d'environnement à partir de 'settings_backup.json'"
Write-Output "2. Relancer votre pipeline de déploiement Azure DevOps pour remettre le code."
