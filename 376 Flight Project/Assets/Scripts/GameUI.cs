using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using TMPro;

public class GameUI : MonoBehaviour
{
    private GameObject CokeHolder, WeedHolder, MethHolder;
    private GameObject CokeText, WeedText, MethText, DistanceText, WinText;
    private GameObject player;
    private AudioSource audioBearRoar;
    private int cokeAmt, weedAmt, methAmt;
    public bool gameWon = false;

    // Start is called before the first frame update
    void Start()
    {
        CokeHolder = GameObject.Find("CokeHolder");
        WeedHolder = GameObject.Find("WeedHolder");
        MethHolder = GameObject.Find("MethHolder");

        CokeText = GameObject.Find("CokeText");
        WeedText = GameObject.Find("WeedText");
        MethText = GameObject.Find("MethText");

        DistanceText = GameObject.Find("DistanceText");
        WinText = GameObject.Find("WinText");

        player = GameObject.Find("PlayerBear");

        audioBearRoar = GetComponent<AudioSource>();
    }

    // Update is called once per frame


    void FixedUpdate()
    {
        cokeAmt = CokeHolder.GetComponentsInChildren<CocaineBrickScript>().Length;
        weedAmt = WeedHolder.GetComponentsInChildren<CannabisScript>().Length;
        methAmt = MethHolder.GetComponentsInChildren<MethBagScript>().Length;

        CokeText.GetComponent<TMP_Text>().SetText("Remaining Coke: " + cokeAmt);
        WeedText.GetComponent<TMP_Text>().SetText("Remaining Weed: " + weedAmt);
        MethText.GetComponent<TMP_Text>().SetText("Remaining Meth: " + methAmt);

        DistanceText.GetComponent<TMP_Text>().SetText("Closest Drug: " + Mathf.Round(closestPickup()));

        if (cokeAmt == 0 && weedAmt == 0 && methAmt == 0 && !gameWon)
        {
            WinGame();
        }
    }

    private void WinGame()
    {
        gameWon = true;
        WinText.GetComponent<Text>().enabled = true;
        audioBearRoar.Play();
        Invoke("BackToStart", 5f);
    }

    private void BackToStart()
    {
        SceneManager.LoadScene("StartMenu");
    }

    private float closestPickup()
    {
        float distance = 1000000000f;

        foreach (Transform tr in CokeHolder.transform)
        {
            if (distance > Mathf.Abs(Vector3.Distance(tr.position, player.transform.position)))
            {
                distance = Vector3.Distance(tr.position, player.transform.position);
            }
        }
        foreach (Transform tr in WeedHolder.transform)
        {
            if (distance > Mathf.Abs(Vector3.Distance(tr.position, player.transform.position)))
            {
                distance = Vector3.Distance(tr.position, player.transform.position);
            }
        }
        foreach (Transform tr in MethHolder.transform)
        {
            if (distance > Mathf.Abs(Vector3.Distance(tr.position, player.transform.position)))
            {
                distance = Vector3.Distance(tr.position, player.transform.position);
            }
        }

        return distance;
    }
}
