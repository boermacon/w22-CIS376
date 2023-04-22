using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MethBagScript : MonoBehaviour
{
    public float attackDamageIncrease = 1;

    void OnTriggerEnter (Collider other)
    {
        if (other.CompareTag("Player"))
        {
            Pickup(other);
        }
    }

    void Pickup(Collider player)
    {
        Debug.Log("Meth bag picked up");
        //Add eating sound effect?

        //Meth increases attack damage
        PlayerController playerStats = player.GetComponent<PlayerController>();
        playerStats.attackDamage = playerStats.attackDamage + attackDamageIncrease;

        Destroy(gameObject);
    }
}
