package ChatApp;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Polygon;
import java.awt.RenderingHints;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Path2D;

import javax.swing.BoxLayout;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.UIManager;

public class ChatTag extends JPanel {
	String who;
	public ChatTag(JLabel content, String w) {
		who = w;
		setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		add(content);
		setOpaque(false);
	}
	 @Override
     public Insets getInsets() {
         return new Insets(10, 10, 10, 10);
     }

     @Override
     protected void paintComponent(Graphics g) {
         //super.paintComponent(g);
    	 Graphics2D g2d = (Graphics2D) g;
         int w = getWidth(), h = getHeight();
         if(who.equals("person")) {
        	 g2d.setPaint(new Color(37, 211, 102));
         }
         else {
        	 g2d.setPaint(new Color(185, 193, 249));
         }
         
         g2d.fillRoundRect(0, 0, w, h, 30, 30);
    	 if(who.equals("robot")) {
             g2d.fillRect((int)(-10*window.scale), h-(int)(20*window.scale), (int)(50*window.scale), (int)(50*window.scale));
    	 }
    	 else {
    		 
             g2d.fillRect(w-(int)(10*window.scale), h-(int)(10*window.scale), (int)(200*window.scale), (int)(200*window.scale));
    	 }
         
     }
     public static void main(String[] args) {
    	 EventQueue.invokeLater(new Runnable() {
             @Override
             public void run() {
                 

                 JPanel testPane = new JPanel();
                 testPane.setBackground(new Color(243, 233, 210));
                 //testPane.setLayout(new GridBagLayout());
                 testPane.add(new ChatTag(new JLabel("Hi! What's up?"),"robot"));
                 testPane.setPreferredSize(new Dimension(500,500));
                 
                 
                 JFrame frame = new JFrame("Testing");
                 frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                 frame.setLayout(new BorderLayout());
                 frame.add(testPane);
                 frame.pack();
                 frame.setLocationRelativeTo(null);
                 frame.setVisible(true);
             }
         });
     }

}
