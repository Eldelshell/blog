package osuya.example;

import java.util.concurrent.Future;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Service;

@Service
public class ASyncServiceImpl implements ASyncService {
	
	@Autowired NormalService normalService;

	@Async
	@Override
	public Future<Boolean> async() {
		
		System.out.println("Managed bean injected: " + (normalService != null));
		
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		System.out.println("I'm done!");
		
		return new AsyncResult<Boolean>(true);
	}

}
