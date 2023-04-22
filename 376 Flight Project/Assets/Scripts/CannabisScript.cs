using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CannabisScript : MonoBehaviour
{
    public float jumpForceIncrease = 100;

    void OnTriggerEnter (Collider other)
    {
        if (other.CompareTag("Player"))
        {
            Pickup(other);
        }
    }

    void Pickup(Collider player)
    {
        Debug.Log("Weed picked up");
        //Add eating sound effect?

        //Weed increases jump height
        PlayerController playerStats = player.GetComponent<PlayerController>();
        playerStats.jumpForce = playerStats.jumpForce + jumpForceIncrease;

        Destroy(gameObject);
    }
}
