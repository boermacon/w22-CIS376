using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class SoundManager : MonoBehaviour
{
    public Image soundOnIcon;
    public Image soundOffIcon;
    public static bool mutedBG = false;

    // Start is called before the first frame update
    void Start()
    {
        UpdateButtonIcon();
    }

    public void OnButtonPress()
    {
        if(!mutedBG)
        {
            mutedBG = true;
        }
        else
        {
            mutedBG = false;
        }
        UpdateButtonIcon();
    }

    private void UpdateButtonIcon()
    {
        if(!mutedBG)
        {
            soundOnIcon.enabled = true;
            soundOffIcon.enabled = false;
        }
        else
        {
            soundOnIcon.enabled = false;
            soundOffIcon.enabled = true;
        }
    }
}
