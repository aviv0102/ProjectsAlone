import java.io.*;
public class ExampleTable {
	public static void  main(String[] args) {
		HighScoresTable table=new HighScoresTable(4);
		HighScoresTable table2=new HighScoresTable(4);

		for(int i=0;i<4;i++){
			ScoreInfo info=new ScoreInfo("aviv",10);
			table.add(info);
		}
		File k=new File("k.txt");
		File a=new File("a.txt");
		try{
		table.save(k);
		table.load(k);
		table2=HighScoresTable.loadFromFile(k);
		table2.save(a);
		table2.load(a);
		}catch(Exception e){
			
		}
		
	}
}
