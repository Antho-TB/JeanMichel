<#
.SYNOPSIS
    Script pour arrêter automatiquement les bases de données PostgreSQL Flexible Server.
.DESCRIPTION
    À utiliser dans un Runbook "Azure Automation" (PowerShell 7.2) avec une identité managée (Managed Identity) configurée.
#>

try {
    Write-Output "Connexion à Azure via l'Identité Managée..."
    Connect-AzAccount -Identity
}
catch {
    Write-Error -Message $_.Exception
    throw
}

# Liste des bases à arrêter (ResourceGroupName, ServerName)
$databases = @(
    @{ ResourceGroup = "rg-dtpf-psql-prod"; Name = "psql-dtpf-psql-prod" },
    @{ ResourceGroup = "rg-dtpf-psql-dev"; Name = "psql-dtpf-psql-dev" }
)

foreach ($db in $databases) {
    Write-Output "Vérification de la base PostgreSQL : $($db.Name) dans $($db.ResourceGroup)..."
    
    $server = Get-AzPostgreSqlFlexibleServer -ResourceGroupName $db.ResourceGroup -Name $db.Name -ErrorAction SilentlyContinue
    
    if ($null -ne $server) {
        if ($server.State -eq "Ready") {
            Write-Output "Base de données $($db.Name) est en cours d'exécution. Arrêt en cours..."
            Stop-AzPostgreSqlFlexibleServer -ResourceGroupName $db.ResourceGroup -Name $db.Name -Force
            Write-Output "Arrêt de $($db.Name) terminé."
        }
        else {
            Write-Output "Ignoré : La base de données $($db.Name) est déjà à l'état $($server.State)."
        }
    }
    else {
        Write-Warning "Serveur $($db.Name) introuvable dans le groupe de ressources $($db.ResourceGroup)."
    }
}

Write-Output "Traitement terminé."
