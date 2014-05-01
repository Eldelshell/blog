package osuya.example;

import java.util.concurrent.Future;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class Spring4Tasks {

	@Autowired ASyncService asyncService;
	
	@Autowired NormalService normalService;
	
	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("/spring.xml");
		Spring4Tasks app = context.getBean(Spring4Tasks.class);
		app.start();
		System.exit(0);
	}
	
	public void start() {
		normalService.notAsync();
		
		Future<Boolean> result = asyncService.async();
		
		for(int i = 0; i < 5; i++) normalService.notAsync();
		
		while(!result.isDone()){
			// we wait
		}
		
	}

}
