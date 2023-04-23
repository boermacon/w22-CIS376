using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HealthManager : MonoBehaviour
{
    public Image healthBar;
    public PlayerController player;
    private float currentHealth;
    private float maxHealth;

    // Start is called before the first frame update
    void Start()
    {
        maxHealth = PlayerController.maxHealth;
    }

    // Update is called once per frame
    void Update()
    {
        currentHealth = player.currentHealth;
        healthBar.fillAmount = player.currentHealth / PlayerController.maxHealth;
    }
}
