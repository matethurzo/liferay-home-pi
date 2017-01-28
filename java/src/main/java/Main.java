import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import com.mashape.unirest.request.GetRequest;
import com.mashape.unirest.request.HttpRequest;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.List;

/**
 * @author Akos Thurzo
 */
public class Main {
	public static void main(String[] args) throws Exception {
		String serialNumber = "serialnumber-4";

		long deviceId = addDevice(serialNumber);

		for (int i = 0; i < 10; i++) {
			uploadData(deviceId, "TEMPERATURE", System.currentTimeMillis());
			uploadData(deviceId, "HUMIDITY", System.currentTimeMillis());
			Thread.sleep(5000);
		}

	}

	private static void uploadData(long deviceId, String type, double value) throws UnirestException {
		JSONObject dataObject = new JSONObject();
		dataObject.put("type", type);
		dataObject.put("value", value);

		HttpResponse<JsonNode> jsonResponse = Unirest.post("http://app.liferay-home.wedeploy.io/sensor-data")
			.header("content-type", "application/json")
			.header("accept", "application/json")
			.body(dataObject)
			.asJson();

		jsonResponse = Unirest.put("http://app.liferay-home.wedeploy.io/sensor-data/" + jsonResponse.getBody().getObject().getLong("id") + "/device")
			.header("content-type", "text/uri-list")
			.header("accept", "application/json")
			.body("http://app.liferay-home.wedeploy.io/devices/" + deviceId)
			.asJson();
	}

	private static long addDevice(String serialNumber) throws UnirestException {
		HttpRequest deviceResponse = Unirest.get("http://app.liferay-home.wedeploy.io/devices/search/findBySerialNumber")
			.queryString("serialNumber", serialNumber);

		HttpResponse<JsonNode> jsonNodeHttpResponse = deviceResponse.asJson();

		JSONArray devices = (JSONArray)((JSONObject) jsonNodeHttpResponse.getBody().getObject().get("_embedded")).get("devices");

		if (devices.length() <= 0) {
			JSONObject device = new JSONObject();
			device.put("name", serialNumber);
			device.put("serialNumber", serialNumber);
			device.put("type", "HOME");

			HttpResponse<JsonNode> response = Unirest.post("http://app.liferay-home.wedeploy.io/devices")
				.header("content-type", "application/json")
				.header("accept", "application/json")
				.body(device)
				.asJson();

			return response.getBody().getObject().getLong("id");
		}
		else {
			return (Integer)((JSONObject)devices.get(0)).get("id");
		}
	}
}
