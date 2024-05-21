import urllib.request
import json
import subprocess


#------------------------------------------------#
#---- Définition des fonctions et procédures ----#
#------------------------------------------------#

# Fonction qui retourne la liste des utilisateurs:
def getData(url):

    # Ouverture de l'URL:
    reponse = urllib.request.urlopen(url)
    data = reponse.read()

    # Décodage des données en JSON:
    data_json = json.loads(data)
    return data_json


# Procédure qui permet d'afficher les noms et prénoms des utilisateurs renvoyés par l'API:
def viewUsers(data):
    for user in data:
        print(f"Nom : {user['nom']}, Prénom : {user['prenom']}")


# Fonction qui retourne les statistiques des utilisateurs:
def statUsers(data):
    # Nombre d'employés:
    nombre_employe = len(data)

    # Récupérer le nombre de groupes distincts:
    # Utilisation d'Internet : https://www.w3schools.com/python/ref_func_set.asp
    groupes = set(user['groupe'] for user in data)
    nombre_groupes = len(groupes)

    # Récupère le nom de domaine:
    # Utilisation d'Internet : https://www.w3schools.com/python/ref_string_split.asp
    echantillon_email = data[0]['email']
    nom_domaine = echantillon_email.split('@')[-1]

    return nombre_employe, nombre_groupes, nom_domaine


# Initie une commande PowerShell:
def execute_powershell(cmd):
    resultat = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    return resultat.stdout


# Fonction pour effectuer le "ls" sous linux:
def ls_powershell(cmd):
    cmd = "Get-ChildItem"
    return execute_powershell(cmd)


# Fonction qui permet de créer les utilisateurs et de les ajouter aux groupes via des commandes PowerShell:
def createUsers(data):
    groupes_crees = set()

    for user in data:
        groupe = user['groupe']

        # Crée le groupe si nécessaire:
        if groupe not in groupes_crees:
            cree_groupe_cmd = f"New-ADGroup -Name '{groupe}' -GroupScope Global -Path 'OU=Groups,DC=farrokhq,DC=com'"
            execute_powershell(cree_groupe_cmd)
            groupes_crees.add(groupe)

        # Crée l'utilisateur avec ses caractéristiques:
        user_cmd = (
            f"New-ADUser -Name '{user['prenom']} {user['nom']}' "
            f"-GivenName '{user['prenom']}' -Surname '{user['nom']}' "
            f"-SamAccountName '{user['login']}' -UserPrincipalName '{user['login']}@farrokhq.com' "
            f"-Path 'OU=Users,DC=farrokhq,DC=com' -AccountPassword (ConvertTo-SecureString '{user['password']}' -AsPlainText -Force) "
            f"-Enabled $true"
        )
        execute_powershell(user_cmd)

        # Ajout de l'utilisateur au groupe:
        ajouter_user = f"Add-ADGroupMember -Identity '{groupe}' -Members '{user['login']}'"
        execute_powershell(ajouter_user)


# Procédure pour faire afficher le menu de séléction:
def afficheMENU():
    print("\n#--------------#\n#---- MENU ----#\n#--------------#\n")
    print("Taper 1 : Affiche les noms et prénoms :")
    print("Taper 2 : Afficher les statistiques :")
    print("Taper 3 : Affichage du répertoire courant :")
    print("Taper 4 : Création des utilisateurs et ajout aux groupes :\n")
    print("F: pour finir\n")


#-----------------------------#
#---- Programme principal ----#
#-----------------------------#

# Définition de l'URL de l'API:
myUrl = "http://srv-peda.iut-acy.local/hoarauju/sae204/users/apiUsers.php?id_sae=13&id_grp=a2&login_usmb=farrokhq"
donnees = getData(myUrl)

# Ouverture du menu de sléction:
fini = False
while fini == False:
    afficheMENU()
    choix = input("Votre choix: ")

# Définition de l'URL de l'API:
    if choix == '1':
        print("\nAffiche les noms et prénoms :\n")
        viewUsers(donnees)

# Affichage des statistiques:
    elif choix == '2':
        print("\nAfficher les statistiques :\n")
        stats = statUsers(donnees)
        print(f"Nombre d'employés: {stats[0]}\nNombre de groupes: {stats[1]}\nNom de domaine : {stats[2]}")

#Exécution de la commande PowerShelle équivalente au "ls" dans un environnement Linux:
    elif choix == '3':
        print("\nAffichage du répertoire courant :")
        ls_output = ls_powershell(donnees)
        print(ls_output)

# Création des utilisateurs et ajout aux groupes:
    elif choix == '4':
        print("\nCréation des utilisateurs et ajout aux groupes :\n")
        createUsers(donnees)

# Fermeture du menu:
    elif (choix == 'F') or (choix == 'f'):
        fini = True

print ('\033[1m' + 'Fin du programme')


#----------------------------#
#----- FIN DU PROGRAMME -----#
#---- QUENTIN FARROKHIAN ----#
#---------- RT1_A2 ----------#
#----------------------------#