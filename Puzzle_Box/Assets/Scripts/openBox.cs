using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class openBox : MonoBehaviour {
    public bool locked = true;
    public GameObject box;
    public GameObject thisButton;
    public GameObject closeButton;
    public GameObject contButton1;
    public GameObject contButton2;
    public AudioSource speaker;
    public AudioClip unlockSound;
    public AudioClip openSound1;
    public AudioClip openSound2;


	//// Use this for initialization
	//void Start () {
		
	//}
	
	//// Update is called once per frame
	//void Update () {
		
	//}

    public void Unlock()
    {
        locked = false;
        speaker.PlayOneShot(unlockSound, 0.7F);
    }

    public void Open()
    {
        if (!locked)
        {
            box.SetActive(true);
            closeButton.SetActive(true);
            contButton1.SetActive(true);
            contButton2.SetActive(true);
            thisButton.SetActive(false);
            speaker.PlayOneShot(openSound1, 0.7F);
            speaker.PlayOneShot(openSound2, 0.7F);
        }
    }
}
