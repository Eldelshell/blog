package osuya.example;

import org.springframework.stereotype.Service;

@Service
public class NormalServiceImpl implements NormalService {

	@Override
	public void notAsync() {
		System.out.println("Not in a thread");
	}

}
