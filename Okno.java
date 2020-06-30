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
	
	JFrame frame = new JFrame();
	
	JLabel oznaka1 = new JLabel();
	JLabel oznaka2 = new JLabel();
	
	JButton gumb1 = new JButton("Ok");  
	JButton gumb2 = new JButton("Reset");   
	
	
	public Okno() {
		// frame settings
		frame.getContentPane().setBackground(Color.WHITE);
		frame.setSize(SIRINA,VISINA);    
		frame.setLayout(null);    
		frame.setVisible(true);
		frame.setLocationRelativeTo(null); // is centered
		frame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
		   
		gumb1.setBounds((int) (SIRINA / 5), 90, 100, 30); // lahko premikas gumb z prvimi dvemi koordinatami, z zadnjimi dvemi velikost
		gumb2.setBounds((int) (SIRINA / 5), 150, 100, 30); 
		
		// labels: text and bounds
		oznaka1.setText("vs Ai");
		oznaka1.setBounds(SIRINA/3, 60, 100, 30);
		
		oznaka2.setText("vs Player");
		oznaka2.setBounds(SIRINA/3, 120, 100, 30);
		


		gumb1.addActionListener(new ActionListener() {
			// gets info from text fields, and updates data
			@Override
			public void actionPerformed(ActionEvent arg0) {
					new KrizecKrozecGrafika1();
			}       
	      });
		
		gumb2.addActionListener(new ActionListener() {
			// resets all data
			public void actionPerformed(ActionEvent arg0) {
					new KrizecKrozecGrafika2();
			}          
		  });

		// add everything on frame
		frame.add(oznaka1); frame.add(oznaka2);
		frame.add(gumb1);     
		frame.add(gumb2);
		frame.repaint();
	}
	

	public static void main(String[] args) {
		new Okno();
	}
}