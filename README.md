# 🕵️ Μια νύχτα στο "palermo"
Είναι μια ψηφιακή υλοποίηση του κλασικού και γνωστού παιχνιδιού "Μια Νύχτα στο Παλέρμο", σχεδιασμένη για να διευκολύνει τη ροή του παιχνιδιού, τη μοιρασιά των ρόλων και τον συντονισμό των γύρων χωρίς την ανάγκη για χαρτί, στυλό και κάποιον τρίτο που λέει τα λόγια.

## Περιγραφοί των ρόλων
Το «Μια Νύχτα στο Παλέρμο» είναι ένα παιχνίδι στρατηγικής, μυστηρίου και ψυχολογίας. Οι παίκτες χωρίζονται σε κρυφούς ρόλους:

- Δολοφόνοι (Μαφία): Προσπαθούν να εξοντώσουν τους πολίτες χωρίς να αποκαλυφθούν.

- Αστυνόμος: Προσπαθεί να ανακαλύψει την ταυτότητα των δολοφόνων.

- Ρουφιάνος / Μέντιουμ: (Προαιρετικοί ρόλοι) Βοηθούν με τις δικές τους ειδικές ικανότητες.

- Τρέλα: Προσπαθεί να βγεί από το παιχνίδι, μέσω ψηφοφορίας, όσο πιο νωρίς γίνεται για να νικήσει. 

- Αθώοι Πολίτες: Προσπαθούν να βρουν ποιοι είναι οι δολοφόνοι μέσα από συζήτηση και ψηφοφορίες κατά τη διάρκεια της «ημέρας».

## Λειτουργίες
- Αυτόματη Διανομή Ρόλων: Κάθε παίκτης βλέπει τον ρόλο του στην οθόνη με απόλυτη μυστικότητα.

- Ψηφιακός Συντονιστής (Narrator): Η εφαρμογή αναλαμβάνει τον ρόλο του αφηγητή, καθοδηγώντας τους παίκτες για το πότε "κοιμάται" και πότε "ξυπνάει" η πόλη.

- Σύστημα Ψηφοφορίας: Εύκολη καταμέτρηση ψήφων κατά τη διάρκεια της ημέρας για την αποκάλυψη των υπόπτων.

- Προσαρμόσιμοι Κανόνες: Επιλογή αριθμού δολοφόνων, εισαγωγή ειδικών ρόλων και ρύθμιση του χρόνου συζήτησης.

## Εγκατάσταση Εφαρμογής
### Για το Android

 - Κατέβασε το `.apk` αρχείο
 - Εφόσον κατέβει πάτα το, και πάτα `install`
 - Θα ξες όταν κατέβηκε, επειδή η μπάρα θα έχει γεμίσει και θα λέει "Open". 
> Αν σας εμφανιστεί προειδοποίηση από το Play Protect για "άγνωστο δημιουργό", μην ανησυχήσετε. Είναι μια αυτόματη ειδοποίηση της Google για εφαρμογές εκτός Play Store. Η εφαρμογή είναι [ασφαλής και καθαρή](##Άδεια λογισμικού).
 

<details>
<summary><h3>Από τον Πηγαίο Κώδικα (ΕΝ)</h3></summary>

- Setup WSL or do this in a Linux machine.
- Clone the `palermo` repository locally.
    ``` bash
    $ git clone https://www.github.com/theolaos/palermo.git
    ```    
- Install all of these system packages for Buildozer:
    - Fedora
    ```bash
    $ sudo dnf update
    $ sudo dnf groupinstall -y "Development Tools" "Development Libraries"
    $ sudo dnf install -y git zip unzip java-17-openjdk-devel python3-pip \
      python3-virtualenv cmake libffi-devel openssl-devel gettext    
    ```
    - Ubuntu
    ```bash
    $ sudo apt update
    $ sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
      python3-virtualenv autoconf libtool pkg-config zlib1g-dev \
      libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev \
      libssl-dev automake autopoint gettext
    ```
- Change to the app directory
    ``` bash
    $ cd palermo
    ```
- Create a virtual python enviroment and then activate it:
    ```bash
    $ python -m venv .venv
    ```
    - linux
    ```bash
    $ source ./.venv/bin/activate
    ```
    - Windows
    ```bash
    $ .\.venv\Scripts\Activate.ps1
    ```
- Download the requirements:

    Using pip:
    ```bash
    (source) $ pip install -r requirements.txt
    ```
    Using your package manager manually (apt, dnf, pacman ...):
    ```bash
    (source) $ sudo 'your-package-manager' install pygame3-'your-package'
    ```
- Initializing buildozer:
    ```bash
    (source) $ buildozer init
    ```
- Make this change to the `include_exts`:
    ```spec
    source.include_exts = py,png,jpg,kv,atlas,ttf
    ```
- Running buildozer:
    ```bash
    (source) $ buildozer -v android debug
    ```    
- After the above command finished find the bin folder and send to your mobile device the `.apk` file.
    
</details>

## Άδεια λογισμικού

Η άδεια του παρόντος λογισμικού είναι η Γενική Άδεια Δημόσιας Χρήσης GNU (GNU General Public License), συγκεκριμένα η έκδοση GNU GPLv3, και περιλαμβάνεται στο αρχείο `LICENSE`.

Το αρχείο `LICENSE` αποτελεί τη δεσμευτική άδεια που εφαρμόζεται σε ολόκληρο το έργο *palermo*.

Αν δεν γνωρίζεις αγγλικά, μπορείς να διαβάσεις τη μεταφρασμένη (μη επίσημη) έκδοση της άδειας εδώ:
https://mathe.ellak.gr/gpl-3-0-txt/