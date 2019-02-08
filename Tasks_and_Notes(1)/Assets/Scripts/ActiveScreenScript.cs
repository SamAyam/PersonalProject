using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ActiveScreenScript : MonoBehaviour {
    public int activeScreen;
    public GameObject screen1;
    public GameObject screen2;
    public GameObject screen3;
    public GameObject screen4;
    public GameObject screen5;
    public GameObject screen6;
    public GameObject screen7;
    public GameObject screen8;
    public GameObject screen9;
    public GameObject screen10;
    public GameObject screen11;

    public GameObject optionsScreen1;
    public GameObject optionsScreen2;
    public GameObject optionsScreen3;
    public GameObject optionsScreen4;
    public GameObject optionsScreen5;

    private void OnEnable()
    {
        TurnOffOptions();
    }

    public void TurnOnOptions()
    {
        if (optionsScreen1 != null) { optionsScreen1.SetActive(true); }
        if (optionsScreen2 != null) { optionsScreen2.SetActive(true); }
        if (optionsScreen3 != null) { optionsScreen3.SetActive(true); }
        if (optionsScreen4 != null) { optionsScreen4.SetActive(true); }
        if (optionsScreen5 != null) { optionsScreen5.SetActive(true); }
    }

    public void TurnOffOptions()
    {
        if (optionsScreen1 != null) { optionsScreen1.SetActive(false); }
        if (optionsScreen2 != null) { optionsScreen2.SetActive(false); }
        if (optionsScreen3 != null) { optionsScreen3.SetActive(false); }
        if (optionsScreen4 != null) { optionsScreen4.SetActive(false); }
        if (optionsScreen5 != null) { optionsScreen5.SetActive(false); }
    }

    private void Update()
    {
        if (activeScreen == 0) { }
        else if (activeScreen == 1)
        {
            screen1.SetActive(true);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
        }
        else if (activeScreen == 2)
        {
            screen1.SetActive(false);
            screen2.SetActive(true);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
        }
        else if (activeScreen == 3)
        {
            screen1.SetActive(false);
            screen2.SetActive(false);
            screen3.SetActive(true);
            screen4.SetActive(false);
            screen5.SetActive(false);
        }
        else if (activeScreen == 4)
        {
            screen1.SetActive(false);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(true);
            screen5.SetActive(false);
        }
        else if (activeScreen == 5)
        {
            screen1.SetActive(false);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(true);
        }
        else if (activeScreen == 6)
        {
            screen1.SetActive(true);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
            screen6.SetActive(true);
            screen7.SetActive(false);
            screen8.SetActive(false);
        }
        else if (activeScreen == 7)
        {
            screen1.SetActive(true);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
            screen6.SetActive(false);
            screen7.SetActive(true);
            screen8.SetActive(false);
        }
        else if (activeScreen == 8)
        {
            screen1.SetActive(true);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
            screen6.SetActive(false);
            screen7.SetActive(false);
            screen8.SetActive(true);
        }
        else if (activeScreen == 9)
        {
            screen1.SetActive(false);
            screen2.SetActive(true);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
            screen9.SetActive(true);
            screen10.SetActive(false);
            screen11.SetActive(false);
        }
        else if (activeScreen == 10)
        {
            screen1.SetActive(false);
            screen2.SetActive(true);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
            screen9.SetActive(false);
            screen10.SetActive(true);
            screen11.SetActive(false);
        }
        else if (activeScreen == 11)
        {
            screen1.SetActive(false);
            screen2.SetActive(true);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
            screen9.SetActive(false);
            screen10.SetActive(false);
            screen11.SetActive(true);
        }
        else
        {
            screen1.SetActive(false);
            screen2.SetActive(false);
            screen3.SetActive(false);
            screen4.SetActive(false);
            screen5.SetActive(false);
        }
    }

    public void SetActiveScreen(int screen)
    {
        activeScreen = screen;
    }
}
