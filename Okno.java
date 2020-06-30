import java.awt.Color;
import java.awt.event.*;
import java.io.File;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.Jokno;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class Okno{

	public static final int SIRINA = 200; // urediš širino Okna
	public static final int VISINA = SIRINA * 16/9; // urediš višino Okna
	
	Jokno okno = new Jokno();
	
	JLabel oznaka1 = new JLabel();
	JLabel oznaka2 = new JLabel();
	
	JButton gumb1 = new JButton("vsAi");  
	JButton gumb2 = new JButton("vsPlayer");   
	
	
	public Okno() {
		okno.getContentPane().setBackground(Color.WHITE);
		okno.setSize(SIRINA,VISINA);    
		okno.setLayout(null);    
		okno.setVisible(true);
		okno.setLocationRelativeTo(null);
		okno.setDefaultCloseOperation(Jokno.HIDE_ON_CLOSE);
		   
		gumb1.setBounds((int) (SIRINA / 5), 90, 100, 30); 
		gumb2.setBounds((int) (SIRINA / 5), 150, 100, 30); 
		 
		oznaka1.setBounds(SIRINA/3, 60, 100, 30);
		oznaka2.setBounds(SIRINA/3, 120, 100, 30);
		


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

		okno.add(oznaka1); okno.add(oznaka2);
		okno.add(gumb1);     
		okno.add(gumb2);
		okno.repaint();
	}
	

	public static void main(String[] args) {
		new Okno();
	}
}