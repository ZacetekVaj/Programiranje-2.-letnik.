import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
/**
 * Krizec Krozec: Grafična različica za dva igralca
 */
@SuppressWarnings("serial")
public class KrizecKrozecGrafika2 extends JFrame {
   // Poimenovane konstante za igralno ploščo
   public static final int VRSTICE = 3;  // VRSTICE krat STOLPCI velikosti celice
   public static final int STOLPCI = 3;
 
   // Poimenovane konstante za razne dimenzije, ki so uporabljene za risanje grafike
   public static final int VELIKOST_CELICE = 100; // širina in višina celice (kvadrat)
   public static final int SIRINA_PLATNA = VELIKOST_CELICE * STOLPCI;  // platno za risanje
   public static final int VISINA_PLATNA = VELIKOST_CELICE * VRSTICE;
   public static final int SIRINA_MREZE = 8;                   // Širina mrežnih črt
   public static final int POLOVICNA_SIRINA_MREZE = SIRINA_MREZE / 2; // Polovična širina mrežnih črt
   // Simbola (križec/krožec) sta prikazana znotraj celice z robno oblogo
   public static final int OBLOGA_CELICE = VELIKOST_CELICE / 6;
   public static final int VELIKOST_SIMBOLA = VELIKOST_CELICE - OBLOGA_CELICE * 2; // širina/višina
   public static final int SIRINA_OBROBE_SIMBOLA = 8; // širina svinčnika
 
   // Uporabljeno je oštevilčenje (notranji razred) za predstavitev raznih stanj v igri
   public enum StanjeIgre {
      IGRANJE, NEODLOCENO, ZMAGA_KRIZEC, ZMAGA_KROZEC
   }
   private StanjeIgre trenutnoStanje;  // trenutno stanje igre
 
   // Uporabljeno je oštevilčenje (notranji razred) za predstavitev vsebin celic
   public enum Celica {
      PRAZNO, KRIZEC, KROZEC
   }
   private Celica trenutniIgralec;  // trenutni igralec
 
   private Celica[][] plosca   ; // Igralna plošča iz VRSTICE-krat-STOLPCI velikosti celic
   private NarisiPlatno platno; // Risalno platno (JPanel) za igralno ploščo
   private JLabel vrsticaStanja;  // vrstica stanja
 
   /** Konstruktor, ki nastavi igro in GUI komponente */
   public KrizecKrozecGrafika2() {
      platno = new NarisiPlatno();  // Sestavi risalno platno ( JPanel)
      platno.setPreferredSize(new Dimension(SIRINA_PLATNA, VISINA_PLATNA));
 
      // Platno (JPanel) sproži MouseEvent ob kliku miške
      platno.addMouseListener(new MouseAdapter() {
         @Override
         public void mouseClicked(MouseEvent e) {  // rokovanje s klikom miške
            int miskaX = e.getX();
            int miskaY = e.getY();
            // Pridobi vrstico in stolpec klika
            int VRSTICEIzbrane = miskaY / VELIKOST_CELICE;
            int STOLPCIIzbrani = miskaX / VELIKOST_CELICE;
 
            if (trenutnoStanje == StanjeIgre.IGRANJE) {
               if (VRSTICEIzbrane >= 0 && VRSTICEIzbrane < VRSTICE && STOLPCIIzbrani >= 0
                     && STOLPCIIzbrani < STOLPCI && plosca[VRSTICEIzbrane][STOLPCIIzbrani] == Celica.PRAZNO) {
                  plosca[VRSTICEIzbrane][STOLPCIIzbrani] = trenutniIgralec; // Naredi potezo
                  posodobiIgro(trenutniIgralec, VRSTICEIzbrane, STOLPCIIzbrani); // posodobi stanje
                  // menjava igralcev
                  trenutniIgralec = (trenutniIgralec == Celica.KRIZEC) ? Celica.KROZEC : Celica.KRIZEC;
               }
            } else {       // konec igre
               pricniIgro(); // resetiranje igre
            }
            // Osvežitev risalnega platna
            repaint();  // Ponoven klic paintComponent().
         }
      });
 
      // Nastavi vrstico stanja (JLabel) za prikaz sporočila stanja
      vrsticaStanja = new JLabel("  ");
      vrsticaStanja.setFont(new Font(Font.DIALOG_INPUT, Font.BOLD, 15));
      vrsticaStanja.setBorder(BorderFactory.createEmptyBorder(2, 5, 4, 5));
 
      Container cp = getContentPane();
      cp.setLayout(new BorderLayout());
      cp.add(platno, BorderLayout.CENTER);
      cp.add(vrsticaStanja, BorderLayout.PAGE_END); // enako kot SOUTH
 
      setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      pack();  // zapakira vse komponente v ta JFrame
      setTitle("Krizec Krozec");
      setVisible(true);  // prikaže ta JFrame
 
      plosca = new Celica[VRSTICE][STOLPCI]; // alocira tabelo
      pricniIgro(); // inicializira igralno ploščo, njeno vsebino in igralne spremenljivke
   }
 
   /** Inicializira igralno ploščo, njeno vsebino in njeno stanje */
   public void pricniIgro() {
      for (int vrstica = 0; vrstica < VRSTICE; ++vrstica) {
         for (int stolpec = 0; stolpec < STOLPCI; ++stolpec) {
            plosca[vrstica][stolpec] = Celica.PRAZNO; // vse celice prazne
         }
      }
      trenutnoStanje = StanjeIgre.IGRANJE; // priprava na igro
      trenutniIgralec = Celica.KRIZEC;       // križec igra prvi
   }
 
   /** Posodobi trenutnoStanje ko je igralec z "taCelica" naredil potezo na
       (VRSTICEIzbrane, STOLPCIIzbrani). */
   public void posodobiIgro(Celica taCelica, int VRSTICEIzbrane, int STOLPCIIzbrani) {
      if (jeZmagal(taCelica, VRSTICEIzbrane, STOLPCIIzbrani)) {  // preveri zmago
         trenutnoStanje = (taCelica == Celica.KRIZEC) ? StanjeIgre.ZMAGA_KRIZEC : StanjeIgre.ZMAGA_KROZEC;
      } else if (jeNeodloceno()) {  // preveri neodločeno
         trenutnoStanje = StanjeIgre.NEODLOCENO;
      }
      // Sicer brez sprememb trenutnega stanja (še vedno StanjeIgre.IGRANJE).
   }
 
   /** Vrne true, če je neodločeno (t.j. nobene prazne celice) */
   public boolean jeNeodloceno() {
      for (int vrstica = 0; vrstica < VRSTICE; ++vrstica) {
         for (int stolpec = 0; stolpec < STOLPCI; ++stolpec) {
            if (plosca[vrstica][stolpec] == Celica.PRAZNO) {
               return false; // prazna celica najdena, ni neodločeno, izhod iz zanke
            }
         }
      }
      return true;  // nobene prazne celice, res neodločeno
   }
 
   /** Vrne true, če je igralec z "taCelica" zmagal ob potezi na
       (VRSTICEIzbrane, STOLPCIIzbrani) */
   public boolean jeZmagal(Celica taCelica, int VRSTICEIzbrane, int STOLPCIIzbrani) {
      return (plosca[VRSTICEIzbrane][0] == taCelica  // 3 v vrsti
            && plosca[VRSTICEIzbrane][1] == taCelica
            && plosca[VRSTICEIzbrane][2] == taCelica
       || plosca[0][STOLPCIIzbrani] == taCelica      // 3 v stolpcu
            && plosca[1][STOLPCIIzbrani] == taCelica
            && plosca[2][STOLPCIIzbrani] == taCelica
       || VRSTICEIzbrane == STOLPCIIzbrani            // 3 v levi diagonali
            && plosca[0][0] == taCelica
            && plosca[1][1] == taCelica
            && plosca[2][2] == taCelica
       || VRSTICEIzbrane + STOLPCIIzbrani == 2  // 3 v desni diagonali
            && plosca[0][2] == taCelica
            && plosca[1][1] == taCelica
            && plosca[2][0] == taCelica);
   }
 
   /**
    *  Notranji razred NarisiPlatno (razširja JPanel) uporabljen za poljubno risanje grafike.
    */
   class NarisiPlatno extends JPanel {
      @Override
      public void paintComponent(Graphics g) {  // klic z repaint()
         super.paintComponent(g);    // zapolne ozadje
         setBackground(Color.WHITE); // nastavi barvo ozadja
 
         // Nariše mrežne črte
         g.setColor(Color.LIGHT_GRAY);
         for (int vrstica = 1; vrstica < VRSTICE; ++vrstica) {
            g.fillRoundRect(0, VELIKOST_CELICE * vrstica - POLOVICNA_SIRINA_MREZE,
                  SIRINA_PLATNA - 1, SIRINA_MREZE, SIRINA_MREZE, SIRINA_MREZE);
         }
         for (int stolpec = 1; stolpec < STOLPCI; ++stolpec) {
            g.fillRoundRect(VELIKOST_CELICE * stolpec - POLOVICNA_SIRINA_MREZE, 0,
                  SIRINA_MREZE, VISINA_PLATNA - 1, SIRINA_MREZE, SIRINA_MREZE);
         }
 
         // Uporabi Graphics2D ki omogoča obrobo (stroke)
         Graphics2D g2d = (Graphics2D)g;
         g2d.setStroke(new BasicStroke(SIRINA_OBROBE_SIMBOLA, BasicStroke.CAP_ROUND,
               BasicStroke.JOIN_ROUND));  // le v Graphics2D
         for (int vrstica = 0; vrstica < VRSTICE; ++vrstica) {
            for (int stolpec = 0; stolpec < STOLPCI; ++stolpec) {
               int x1 = stolpec * VELIKOST_CELICE + OBLOGA_CELICE;
               int y1 = vrstica * VELIKOST_CELICE + OBLOGA_CELICE;
               if (plosca[vrstica][stolpec] == Celica.KRIZEC) {
                  g2d.setColor(Color.GREEN);
                  int x2 = (stolpec + 1) * VELIKOST_CELICE - OBLOGA_CELICE;
                  int y2 = (vrstica + 1) * VELIKOST_CELICE - OBLOGA_CELICE;
                  g2d.drawLine(x1, y1, x2, y2);
                  g2d.drawLine(x2, y1, x1, y2);
               } else if (plosca[vrstica][stolpec] == Celica.KROZEC) {
                  g2d.setColor(Color.BLUE);
                  g2d.drawOval(x1, y1, VELIKOST_SIMBOLA, VELIKOST_SIMBOLA);
               }
            }
         }
 
         // Izpiše sporočila v vrstici stanja
         if (trenutnoStanje == StanjeIgre.IGRANJE) {
            vrsticaStanja.setForeground(Color.RED);
            if (trenutniIgralec == Celica.KRIZEC) {
               vrsticaStanja.setText("Krizec je na vrsti");
            } else {
               vrsticaStanja.setText("Krozec je na vrsti");
            }
         } else if (trenutnoStanje == StanjeIgre.NEODLOCENO) {
            vrsticaStanja.setForeground(Color.RED);
            vrsticaStanja.setText("Neodloceno! Kliknite za ponovno igro.");
         } else if (trenutnoStanje == StanjeIgre.ZMAGA_KRIZEC) {
            vrsticaStanja.setForeground(Color.RED);
            vrsticaStanja.setText("Krizec je zmagal! Kliknite za ponovno igro.");
         } else if (trenutnoStanje == StanjeIgre.ZMAGA_KROZEC) {
            vrsticaStanja.setForeground(Color.RED);
            vrsticaStanja.setText("Krozec je zmagal! Kliknite za ponovno igro.");
         }
      }
   }
 
   /** Glavna main() metoda */
   public static void main(String[] args) {
      // Zažene GUI kodo v Event-Dispatching niti za nitno varnost
      SwingUtilities.invokeLater(new Runnable() {
         @Override
         public void run() {
            new KrizecKrozecGrafika2(); // Konstruktor naredi svoje delo
         }
      });
   }
}