use serde::{Deserialize, Serialize};
use std::io::prelude::*;
use std::net::{TcpListener, TcpStream};
use std::thread;

#[derive(Serialize, Deserialize, Debug)]
struct GameResult {
    #[serde(rename = "Dealer's Score")]
    dealer_score: u32,
    #[serde(rename = "Winning Players")]
    winning_players: Vec<String>,
}

fn handle_client(mut stream: TcpStream) {
    let mut data = [0; 1024];
    match stream.read(&mut data) {
        Ok(size) => {
            let received_str = String::from_utf8_lossy(&data[..size]).to_string();
            let received_data: serde_json::Value = serde_json::from_str(&received_str).unwrap();

            let player_id = received_data["player_id"].as_str().unwrap().to_string();
            let game_result: GameResult = serde_json::from_value(received_data["game_result"].clone()).unwrap();

            println!("{}'s Score: {}", player_id, game_result.dealer_score);
            println!("Winning Players: {:?}", game_result.winning_players);
        }
        Err(e) => {
            println!("Failed to receive data: {:?}", e);
        }
    }
}

fn main() {
    let listener = TcpListener::bind("0.0.0.0:9999").expect("Failed to bind address");
    println!("Server is waiting for player connections...");

    let mut player_count = 0;

    for stream in listener.incoming() {
        match stream {
            Ok(mut stream) => {
                player_count += 1;

                if player_count > 2 {
                    println!("Maximum player limit reached. Spectator at address {:?}", stream.peer_addr());
                    break; // Stop accepting more connections
                }

                let player_id = match player_count {
                    1 => "Player 1".to_string(),
                    2 => "Player 2".to_string(),
                    _ => "Spectator".to_string(),
                };

                let addr = stream.peer_addr().expect("Couldn't get peer address");
                println!("Connected to {} at address {}", player_id, addr);

                let encoded_id = player_id.as_bytes();
                stream.write_all(encoded_id).expect("Failed to send player ID to client");

                let handle = thread::spawn(move || {
                    handle_client(stream);
                });

                handle.join().expect("Thread panicked");
            }
            Err(e) => {
                println!("Error: {}", e);
            }
        }
    }
}
