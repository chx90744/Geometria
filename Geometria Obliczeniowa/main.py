import streamlit as st
import matplotlib.pyplot as plt
import random

def iloczyn_wektorowy(X, Y, Z):
    """Oblicza iloczyn wektorowy wektorów XZ i XY."""
    x1 = Z[0] - X[0]
    y1 = Z[1] - X[1]
    x2 = Y[0] - X[0]
    y2 = Y[1] - X[1]
    return x1 * y2 - x2 * y1

def sprawdz(X, Y, Z):
    """Sprawdza, czy punkt Z leży na odcinku XY."""
    return (min(X[0], Y[0]) <= Z[0] <= max(X[0], Y[0])) and \
           (min(X[1], Y[1]) <= Z[1] <= max(X[1], Y[1]))

def znajdz_przedzial_pokrywania(A, B, C, D):
    """Znajduje punkty końcowe wspólnego odcinka dla odcinków współliniowych."""
    punkty = []
    
    # Sprawdź które punkty końcowe leżą na przeciwnych odcinkach
    if sprawdz(A, B, C):
        punkty.append(C)
    if sprawdz(A, B, D):
        punkty.append(D)
    if sprawdz(C, D, A):
        punkty.append(A)
    if sprawdz(C, D, B):
        punkty.append(B)
    
    # Jeśli mniej niż 2 punkty, odcinki tylko stykają się w jednym punkcie
    if len(punkty) < 2:
        return punkty[0] if punkty else None
    
    # Posortuj punkty według współrzędnych
    punkty.sort(key=lambda p: (p[0], p[1]))
    
    # Zwróć skrajne punkty obszaru pokrywania
    return (punkty[0], punkty[-1])

def znajdz_punkt_przeciecia(A, B, C, D):
    """Znajduje punkt przecięcia odcinków AB i CD."""
    denominator = (B[0]-A[0])*(D[1]-C[1]) - (B[1]-A[1])*(D[0]-C[0])
    
    if denominator == 0:  # Odcinki równoległe lub pokrywające się
        return None
    
    t = ((C[0]-A[0])*(D[1]-C[1]) - (C[1]-A[1])*(D[0]-C[0])) / denominator
    s = ((C[0]-A[0])*(B[1]-A[1]) - (C[1]-A[1])*(B[0]-A[0])) / denominator
    
    if 0 <= t <= 1 and 0 <= s <= 1:
        return (A[0] + t*(B[0]-A[0]), A[1] + t*(B[1]-A[1]))
    return None

def czy_przecinaja(A, B, C, D):
    """Sprawdza przecięcie odcinków AB i CD."""
    if A == B:
        return False, None, "ODCINEK_AB_ZEROWY"
    if C == D:
        return False, None, "ODCINEK_CD_ZEROWY"
    
    v1 = iloczyn_wektorowy(C, D, A)
    v2 = iloczyn_wektorowy(C, D, B)
    v3 = iloczyn_wektorowy(A, B, C)
    v4 = iloczyn_wektorowy(A, B, D)

    denominator = (B[0]-A[0])*(D[1]-C[1]) - (B[1]-A[1])*(D[0]-C[0])
    
    # Przypadki skrajne
    if denominator == 0:  # Równoległe lub współliniowe
        if v1 == 0:  # Współliniowe
            # Sprawdź wspólne wierzchołki
            wspolne_punkty = []
            if A == C or A == D:
                wspolne_punkty.append(A)
            if B == C or B == D:
                wspolne_punkty.append(B)
            
            if wspolne_punkty:
                # Znajdź przedział pokrywania
                przedzial = znajdz_przedzial_pokrywania(A, B, C, D)
                if przedzial and isinstance(przedzial, tuple):
                    return True, (wspolne_punkty[0], przedzial), "WSPOLNY_WIERZCHOLEK_I_POKRYWANIE"
                else:
                    return True, wspolne_punkty[0], "WSPOLNY_WIERZCHOLEK"
            
            # Brak wspólnych wierzchołków, ale może być pokrywanie
            przedzial = znajdz_przedzial_pokrywania(A, B, C, D)
            if przedzial:
                if isinstance(przedzial, tuple):
                    return True, przedzial, "POKRYWAJACE_SIE"
                else:
                    return True, przedzial, "PUNKT_NA_ODCINKU"
        return False, None, "ROWNOLEGLE_ROZLACZNE"
    
    # Przecięcie właściwe
    if ((v1 > 0 and v2 < 0 or v1 < 0 and v2 > 0) and 
        (v3 > 0 and v4 < 0 or v3 < 0 and v4 > 0)):
        return True, znajdz_punkt_przeciecia(A, B, C, D), "PRZECIECIE_WLASCIWE"
    
    # Punkty końcowe na odcinkach
    if v1 == 0 and sprawdz(C, D, A):
        return True, A, "PUNKT_NA_ODCINKU"
    if v2 == 0 and sprawdz(C, D, B):
        return True, B, "PUNKT_NA_ODCINKU"
    if v3 == 0 and sprawdz(A, B, C):
        return True, C, "PUNKT_NA_ODCINKU"
    if v4 == 0 and sprawdz(A, B, D):
        return True, D, "PUNKT_NA_ODCINKU"
    
    return False, None, "BRAK_PRZECIECIA"

def rysuj_wykres(A, B, C, D, punkt_przeciecia=None, obszar_pokrywania=None):
    """Generuje wykres z odcinkami i zaznaczonym obszarem przecięcia."""
    fig, ax = plt.subplots()
    
    # Rysowanie odcinków
    ax.plot([A[0], B[0]], [A[1], B[1]], 'b-', label='Odcinek AB', linewidth=2)
    ax.plot([C[0], D[0]], [C[1], D[1]], 'r-', label='Odcinek CD', linewidth=2)
    
    # Zaznaczanie punktów
    for point, label in zip([A, B, C, D], ['A', 'B', 'C', 'D']):
        ax.plot(point[0], point[1], 'ro' if label in ['C','D'] else 'bo')
        ax.text(point[0], point[1], label, fontsize=12, ha='right')
    
    # Obszar pokrywania (dla odcinków współliniowych)
    if obszar_pokrywania:
        p1, p2 = obszar_pokrywania
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'y-', linewidth=4, alpha=0.5, label='Obszar pokrywania')
    
    # Punkt przecięcia
    if punkt_przeciecia:
        ax.plot(punkt_przeciecia[0], punkt_przeciecia[1], 'go', markersize=8, label='Punkt przecięcia')
        ax.text(punkt_przeciecia[0], punkt_przeciecia[1], 
                f'({punkt_przeciecia[0]:.2f}, {punkt_przeciecia[1]:.2f})', 
                fontsize=10, ha='right')
    
    # Konfiguracja wykresu
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)
    ax.legend()
    ax.set_title('Przecięcie odcinków AB i CD')
    
    # Zakres osi
    all_points = [A, B, C, D]
    if punkt_przeciecia:
        all_points.append(punkt_przeciecia)
    if obszar_pokrywania:
        all_points.extend(obszar_pokrywania)
    ax.set_xlim(min(p[0] for p in all_points)-1, max(p[0] for p in all_points)+1)
    ax.set_ylim(min(p[1] for p in all_points)-1, max(p[1] for p in all_points)+1)
    
    return fig

# Interfejs użytkownika
st.title("Analiza przecięcia odcinków")
st.write("Podaj współrzędne punktów lub wylosuj je:")

# Losowanie punktów
def losuj_punkty():
    st.session_state.a_x = random.randint(0, 10)
    st.session_state.a_y = random.randint(0, 10)
    st.session_state.b_x = random.randint(0, 10)
    st.session_state.b_y = random.randint(0, 10)
    st.session_state.c_x = random.randint(0, 10)
    st.session_state.c_y = random.randint(0, 10)
    st.session_state.d_x = random.randint(0, 10)
    st.session_state.d_y = random.randint(0, 10)

# Formularz wprowadzania danych
col1, col2 = st.columns(2)

with col1:
    st.header("Odcinek AB")
    a_x = st.number_input("A - X", value=1, key="a_x")
    a_y = st.number_input("A - Y", value=1, key="a_y")
    b_x = st.number_input("B - X", value=4, key="b_x")
    b_y = st.number_input("B - Y", value=4, key="b_y")

with col2:
    st.header("Odcinek CD")
    c_x = st.number_input("C - X", value=2, key="c_x")
    c_y = st.number_input("C - Y", value=5, key="c_y")
    d_x = st.number_input("D - X", value=5, key="d_x")
    d_y = st.number_input("D - Y", value=2, key="d_y")

st.button("Losuj punkty", on_click=losuj_punkty)

# Przetwarzanie danych
A, B, C, D = (a_x, a_y), (b_x, b_y), (c_x, c_y), (d_x, d_y)
przecinaja, punkt, typ = czy_przecinaja(A, B, C, D)

# Wizualizacja i komunikaty
if typ == "ODCINEK_AB_ZEROWY":
    st.error("Błąd: Punkty A i B są identyczne - nie tworzą odcinka!")
elif typ == "ODCINEK_CD_ZEROWY":
    st.error("Błąd: Punkty C i D są identyczne - nie tworzą odcinka!")
elif typ == "PRZECIECIE_WLASCIWE":
    fig = rysuj_wykres(A, B, C, D, punkt_przeciecia=punkt)
    st.pyplot(fig)
    st.success(f"Odcinki przecinają się w punkcie ({punkt[0]:.2f}, {punkt[1]:.2f})")
elif typ == "WSPOLNY_WIERZCHOLEK":
    fig = rysuj_wykres(A, B, C, D, punkt_przeciecia=punkt)
    st.pyplot(fig)
    st.warning(f"Odcinki mają wspólny punkt w ({punkt[0]:.2f}, {punkt[1]:.2f})")
elif typ == "PUNKT_NA_ODCINKU":
    fig = rysuj_wykres(A, B, C, D, punkt_przeciecia=punkt)
    st.pyplot(fig)
    st.warning(f"Punkt końcowy leży na odcinku w ({punkt[0]:.2f}, {punkt[1]:.2f})")
elif typ == "POKRYWAJACE_SIE":
    p1, p2 = punkt
    fig = rysuj_wykres(A, B, C, D, obszar_pokrywania=(p1, p2))
    st.pyplot(fig)
    st.warning("Odcinki są współliniowe i pokrywają się w przedziale:")
    st.warning(f"Od ({p1[0]:.2f}, {p1[1]:.2f}) do ({p2[0]:.2f}, {p2[1]:.2f})")
elif typ == "ROWNOLEGLE_ROZLACZNE":
    fig = rysuj_wykres(A, B, C, D)
    st.pyplot(fig)
    st.info("Odcinki są równoległe i nie mają punktów wspólnych")
elif typ == "WSPOLNY_WIERZCHOLEK_I_POKRYWANIE":
    wierzcholek, przedzial = punkt
    p1, p2 = przedzial
    fig = rysuj_wykres(A, B, C, D, punkt_przeciecia=wierzcholek, obszar_pokrywania=(p1, p2))
    st.pyplot(fig)
    st.warning("Odcinki mają wspólny punkt w:")
    st.warning(f"({wierzcholek[0]:.2f}, {wierzcholek[1]:.2f})")
    st.warning("Odcinki są współliniowe i pokrywają się w przedziale:")
    st.warning(f"Od ({p1[0]:.2f}, {p1[1]:.2f}) do ({p2[0]:.2f}, {p2[1]:.2f})")    
else:
    fig = rysuj_wykres(A, B, C, D)
    st.pyplot(fig)
    st.info("Odcinki się nie przecinają")

# Sekcja testowa
st.subheader("Przykłady testowe")
st.write("""
| Przypadek               | A      | B      | C      | D      | Oczekiwany wynik |
|-------------------------|--------|--------|--------|--------|------------------|
| Przecięcie właściwe     | (1,1)  | (4,4)  | (1,4)  | (4,1)  | Przecięcie w (2.5,2.5) |
| Równoległe rozłączne    | (1,1)  | (3,3)  | (1,2)  | (3,4)  | Brak przecięcia |
| Pokrywające się         | (1,1)  | (4,4)  | (2,2)  | (3,3)  | Pokrywanie od (2,2) do (3,3) |
| Pionowe równoległe      | (2,1)  | (2,5)  | (3,1)  | (3,5)  | Brak przecięcia |
| Punkt na odcinku        | (1,1)  | (5,5)  | (2,2)  | (2,0)  | Przecięcie w (2,2) |
""")