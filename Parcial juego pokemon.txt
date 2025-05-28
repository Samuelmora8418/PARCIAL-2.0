#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

struct Ataque {
    string nombre;
    int daño;
    int maxUsos;
    int usados;
};

struct Pokemon {
    string nombre;
    int vida;
    Ataque atk1, atk2, atk3;
    int ultimoAtaque;  // 0 = ninguno, 1, 2, 3 o 4 (curar)
};

void mostrarVida(const Pokemon& p) {
    cout << p.nombre << " tiene " << p.vida << " puntos de vida.\n";
}

bool puedeUsar(const Ataque& a) {
    return a.usados < a.maxUsos;
}

void atacar(Pokemon& atacante, Pokemon& defensor) {
    int opcion;

    while (true) {
        cout << "\nTurno de " << atacante.nombre << ". Elige un ataque:\n";

        if (atacante.ultimoAtaque != 1 && puedeUsar(atacante.atk1))
            cout << "1. " << atacante.atk1.nombre << " (" << atacante.atk1.daño << " daño)\n";

        if (atacante.ultimoAtaque != 2 && puedeUsar(atacante.atk2))
            cout << "2. " << atacante.atk2.nombre << " (" << atacante.atk2.daño << " daño)\n";

        if (atacante.ultimoAtaque != 3 && puedeUsar(atacante.atk3))
            cout << "3. " << atacante.atk3.nombre << " (" << atacante.atk3.daño << " daño)\n";

        if (atacante.ultimoAtaque != 4)
            cout << "4. Recuperar vida (15 HP)\n";

        cout << "Opción: ";
        cin >> opcion;

        if (cin.fail()) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Entrada inválida. Intenta de nuevo.\n";
            continue;
        }

        if (opcion == atacante.ultimoAtaque) {
            cout << "No puedes usar el mismo ataque dos veces seguidas.\n";
            continue;
        }

        if (opcion >= 1 && opcion <= 3) {
            Ataque* elegido = nullptr;
            if (opcion == 1) elegido = &atacante.atk1;
            else if (opcion == 2) elegido = &atacante.atk2;
            else elegido = &atacante.atk3;

            if (!puedeUsar(*elegido)) {
                cout << "Ya no quedan usos para ese ataque.\n";
                continue;
            }
            break;
        } else if (opcion == 4) {
            break;
        } else {
            cout << "Opción inválida. Intenta de nuevo.\n";
        }
    }

    if (opcion == 4) {
        atacante.vida += 15;
        if (atacante.vida > 100) atacante.vida = 100;
        cout << atacante.nombre << " se curó 15 puntos de vida.\n";
        mostrarVida(atacante);
        atacante.ultimoAtaque = 4;
        return;
    }

    // 40% probabilidad de fallo
    if (rand() % 100 < 40) {
        cout << atacante.nombre << " falló el ataque.\n";
        atacante.ultimoAtaque = opcion;
        mostrarVida(defensor);
        return;
    }

    Ataque* ataqueUsado = nullptr;
    if (opcion == 1) ataqueUsado = &atacante.atk1;
    else if (opcion == 2) ataqueUsado = &atacante.atk2;
    else ataqueUsado = &atacante.atk3;

    ataqueUsado->usados++;

    defensor.vida -= ataqueUsado->daño;
    if (defensor.vida < 0) defensor.vida = 0;

    cout << atacante.nombre << " usó " << ataqueUsado->nombre << " y causó " << ataqueUsado->daño << " de daño.\n";
    mostrarVida(defensor);

    atacante.ultimoAtaque = opcion;
}

int sorteo() {
    int jugador, computadora;
    cout << "Sorteo: elige un número del 1 al 10: ";
    cin >> jugador;
    if (cin.fail() || jugador < 1 || jugador > 10) {
        cin.clear();
        cin.ignore(1000, '\n');
        jugador = rand() % 10 + 1;
        cout << "Número inválido, se asignó uno al azar: " << jugador << endl;
    }
    computadora = rand() % 10 + 1;
    cout << "La computadora eligió: " << computadora << endl;

    if (jugador == computadora) {
        cout << "¡Empiezas tú!\n";
        return 0;
    } else {
        cout << "Empieza la computadora.\n";
        return 1;
    }
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    Pokemon pikachu;
    pikachu.nombre = "Pikachu";
    pikachu.vida = 100;
    pikachu.atk1 = {"Impactrueno", 20, 3, 0};
    pikachu.atk2 = {"Placaje", 10, 5, 0};
    pikachu.atk3 = {"Rayo", 25, 2, 0};
    pikachu.ultimoAtaque = 0;

    Pokemon charmander;
    charmander.nombre = "Charmander";
    charmander.vida = 100;
    charmander.atk1 = {"Ascuas", 25, 3, 0};
    charmander.atk2 = {"Arañazo", 15, 5, 0};
    charmander.atk3 = {"Garra Dragón", 30, 2, 0};
    charmander.ultimoAtaque = 0;

    mostrarVida(pikachu);
    mostrarVida(charmander);

    int turno = sorteo();

    while (pikachu.vida > 0 && charmander.vida > 0) {
        if (turno == 0) {
            atacar(pikachu, charmander);
            if (charmander.vida <= 0) break;
            turno = 1;
        } else {
            atacar(charmander, pikachu);
            if (pikachu.vida <= 0) break;
            turno = 0;
        }
    }

    cout << (pikachu.vida <= 0 ? "\n¡Charmander gana!\n" : "\n¡Pikachu gana!\n");

    return 0;
}