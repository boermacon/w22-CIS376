using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CocaineBrickScript : MonoBehaviour
{
    public float speedIncrease = 10;

    void OnTriggerEnter (Collider other)
    {
        if (other.CompareTag("Player"))
        {
            Pickup(other);
        }
    }

    void Pickup(Collider player)
    {
        Debug.Log("Cocaine picked up");

        //Cocaine increases run speed
        PlayerController playerStats = player.GetComponent<PlayerController>();
        playerStats.maxSpeed = playerStats.maxSpeed + speedIncrease;

        Destroy(gameObject);
    }
}
