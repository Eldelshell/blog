package osuya.example;

import java.util.concurrent.Future;

public interface ASyncService {

	Future<Boolean> async();
	
}
