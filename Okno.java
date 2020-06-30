import java.awt.Color;
import java.awt.event.*;
import java.io.File;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class Okno{

	public static final int SIRINA = 200; // urediš širino Okna
	public static final int VISINA = SIRINA * 16/9; // urediš višino Okna
	
	JFrame okvir = new JFrame();
	
	JLabel oznaka1 = new JLabel();
	JLabel oznaka2 = new JLabel();
	
	JButton gumb1 = new JButton("vs Ai");  
	JButton gumb2 = new JButton("vs Player");   
	
	
	public Okno() {
		okvir.getContentPane().setBackground(Color.WHITE);
		okvir.setSize(SIRINA,VISINA);    
		okvir.setLayout(null);    
		okvir.setVisible(true);
		okvir.setLocationRelativeTo(null);
		okvir.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
		//premikamo gumbe   
		gumb1.setBounds((int) (SIRINA / 5), 90, 100, 30); 
		gumb2.setBounds((int) (SIRINA / 5), 150, 100, 30); 
		


		gumb1.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
					new KrizecKrozecGrafika1();
			}       
	      });
		
		gumb2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
					new KrizecKrozecGrafika2();
			}          
		  });

		okvir.add(oznaka1); okvir.add(oznaka2);
		okvir.add(gumb1);     
		okvir.add(gumb2);
		okvir.repaint();
	}
	

	public static void main(String[] args) {
		new Okno();
	}
}
