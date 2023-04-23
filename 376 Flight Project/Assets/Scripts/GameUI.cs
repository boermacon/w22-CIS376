using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class GameUI : MonoBehaviour
{
    private GameObject CokeHolder, WeedHolder, MethHolder;
    private GameObject CokeText, WeedText, MethText, DistanceText;
    private GameObject player;
    private int cokeAmt, weedAmt, methAmt;

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

        player = GameObject.Find("PlayerBear");
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
