package ChatApp;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.GridBagLayout;
import java.awt.Image;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.util.Scanner;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.ScrollPaneLayout;
import javax.swing.border.EmptyBorder;

public class window extends JFrame implements ActionListener,KeyListener{
	JTextField text;
	JPanel a1;
	JScrollPane chat_board;
	public static double scale = 1.4;
	Color chat_board_c= new Color(243, 233, 210); 
	//Color chat_board_c = Color.WHITE;
	JPanel p1;//upper green region
	static Box vertical = Box.createVerticalBox();
	private boolean enterPressed = false; 
	Scanner scanner = new Scanner(System.in);

	public window(){
		
		setLayout(null);
		
		//upper green region
		p1 = new JPanel();
		p1.setBackground(new Color(7,94,84));
		p1.setBounds(0,0,(int)(450*scale),(int)(70*scale));
		p1.setLayout(null);
		add(p1);
		
		
		//robot
		ImageIcon bot_icon = new ImageIcon(ClassLoader.getSystemResource("icons/robot.png"));
		
		bot_icon = new ImageIcon(getScaledImage(bot_icon.getImage(),(int)(75*scale),(int)(75*scale)));
		
		JLabel bot = new JLabel(bot_icon);
		bot.setBounds((int)(10*scale),(int)(5*scale),(int)(50*scale),(int)(60*scale));
		p1.add(bot);
		
		
		
		JLabel name = new JLabel("BJTUer");
		name.setBounds((int)(150*scale), (int)(22*scale), (int)(200*scale),(int)(30*scale));
		name.setForeground(Color.WHITE);
		name.setFont(new Font("Dank Mono", Font.BOLD, (int)(30*scale)));
		p1.add(name);
		
		a1 = new JPanel();
		//a1.setBounds(5, 75, 425, 550);
		chat_board = new JScrollPane(a1, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		a1.setBackground(chat_board_c);
		chat_board.setBounds((int)(5*scale), (int)(75*scale), (int)(425*scale), (int)(550*scale));
		
		add(chat_board);
		//chat_board.getViewport().setBackground(new Color(0, 204, 204));
		//add(a1 );
		
		text = new JTextField();
		text.setBounds((int)(5*scale), (int)(630*scale), (int)(357*scale) ,(int)(29 *scale));
		text.setFont(new Font("Dank Mono", Font.BOLD, (int)(16*scale)));
		text.addKeyListener(this);
		add(text);
		
		JButton send = new JButton("Send");
		send.setBounds((int)(363*scale),(int)(630*scale), (int)(65 *scale), (int)(29*scale));
		send.setBackground(new Color(7, 94, 84));
		send.setFont(new Font("Hack NF", Font.BOLD, (int)(16*scale)));
		send.setForeground(Color.WHITE);
		send.addActionListener(this);
		add(send);
		
		addWindowListener(new WindowAdapter() {
	        //for closing
	        @Override
	        public void windowClosing(WindowEvent e) {
	            System.exit(0);
	            //JOptionPane.showMessageDialog(null, "Closing");
	        }
	        //for closed

	        @Override
	        public void windowClosed(WindowEvent e) {
	            System.exit(0);
	        }
	    });
		setSize((int)(450*scale), (int)(700*scale));
		setLocation((int)(200*scale), (int)(50*scale));
		getContentPane().setBackground(Color.WHITE);
		setResizable(false);
		setVisible(true);
		setFocusable(true);
		setFocusTraversalKeysEnabled(false);
		
	}
	
	@Override
	public void keyPressed(KeyEvent e) {
		if(!enterPressed) {
			int key = e.getKeyCode();
		    if(key == KeyEvent.VK_ENTER){
		    	String out = text.getText();
				if(!out.equals("")) {
					add_chat(out,false);
					String res = waiting();
					add_chat(res, true);

				}
		        enterPressed = true; 
		    }
		}
	    
	}
	
	@Override
	public void keyReleased(KeyEvent e) {
		 int key = e.getKeyCode();
		    if(key == KeyEvent.VK_ENTER){
		     
		        enterPressed = false;
		 }
	}
	@Override
	public void keyTyped(KeyEvent e) {
		
	}
	
	private Image getScaledImage(Image srcImg, int w, int h){
	    BufferedImage resizedImg = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
	    Graphics2D g2 = resizedImg.createGraphics();

	    g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
	    g2.drawImage(srcImg, 0, 0, w, h, null);
	    g2.dispose();

	    return resizedImg;
	}
	
	public void actionPerformed(ActionEvent ae) {
		String out = text.getText();
		
		
		if(!out.equals("")) {
			add_chat(out,false);
			//add_chat("hi", true);
			String returned = waiting();
			add_chat(returned, true);
		}
		
		
	}

	String waiting(){
		
		while(!scanner.hasNext()){

		}
		String data = scanner.nextLine();
		return data;
	}
	
	void add_chat(String txt,boolean robot) {
		if(!robot){
			System.out.println(txt);
		}
		
		JPanel p2;
		if(robot) {
			p2 = formatLabel(txt, "robot"); 
		}
		else {
			p2 = formatLabel(txt, "person"); 
		}

		a1.setLayout(new BorderLayout());
		
		JPanel right = new JPanel(new BorderLayout());
		if(robot) {
			right.add(p2, BorderLayout.LINE_START);
		}
		else {
			right.add(p2, BorderLayout.LINE_END);
		}
		right.setBackground(chat_board_c);
		vertical.add(right);
		vertical.add(Box.createVerticalStrut(10));
		
		a1.add(vertical, BorderLayout.PAGE_START);
		chat_board.getVerticalScrollBar().setValue( chat_board.getVerticalScrollBar().getMaximum() );
		a1.revalidate();
		text.setText("");
		repaint();
		invalidate();
		validate();
	}
	
	public JPanel formatLabel(String out, String who) {
		
		out = formatInput(out, 40); 
		JLabel output = new JLabel(out);
		output.setFont(new Font("ACaslonPro-Italic", Font.BOLD, (int)(15*scale)));
		if(who.equals("robot")) {
			output.setBackground(new Color(185, 193, 249));
		}else {
			output.setBackground(new Color(37, 211, 102));
		}
		
		output.setBorder(new EmptyBorder(0 ,(int)(10*scale),0,(int)(10*scale)));
		output.setOpaque(true);
		JPanel panel = new JPanel();
		panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
		if(who.equals("person")) {
			panel.setBorder(new EmptyBorder((int)(5*scale) ,0,0,(int)(5*scale)));
		}
		else {
			panel.setBorder(new EmptyBorder((int)(5*scale) ,(int)(5*scale),0,0));
		}
		panel.add(new ChatTag(output, who));
		
		panel.setBackground(chat_board_c);
		return panel;
		
	}
	
	public static String formatInput(String input, int constr) {
		String formatted = "<html>";
		String[] word_L = input.split(" ");
		
		int count = 0 ;
		int i =0;
		
		while(i<word_L.length) {
			if(word_L[i].length()<constr) {
				if(word_L[i].length() + count < constr) {
					if(count == 0) {
						formatted = formatted.concat(word_L[i]);
						count+= word_L[i].length() ;
					}
					else {
						formatted = formatted.concat(" "+word_L[i]);
						count+= word_L[i].length() + 1 ;
					}
					
					i ++;
				}
				else {
					formatted = formatted.concat("<br/>");
					count = 0;
				}
			}
			else {
				if(count == constr - 1) {
					 formatted = formatted.concat("<br/>");
					 count = 0;
				}
				int index = 0;
				while(index < word_L[i].length()) {
					String buffer;
					if(word_L[i].length() - index + count < constr) {//finish the word spliting
						buffer = word_L[i].substring(index, word_L[i].length());
						formatted = formatted.concat(buffer);
						count += buffer.length();
						index  = word_L[i].length(); // break
					}
					else {
						if(index == 0) {
							buffer = word_L[i].substring(index, index + (constr - count));
							formatted = formatted.concat(" "+buffer+"-" +"<br/>");
							index = index + (constr - count);
						}
						else {
							buffer = word_L[i].substring(index, index + (constr - count));
							formatted = formatted.concat(buffer+"-" +"<br/>");
							index = index + (constr - count);
						}
						count = 0;
						
					}
					
				}
				i++;
			}
		}
		
		formatted.concat("</html>");
		return formatted;
	}
	
	public static void main(String[] args) {
		new window();
	}
}
