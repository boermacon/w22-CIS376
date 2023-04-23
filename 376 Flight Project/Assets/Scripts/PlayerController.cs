using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

//using Hashtable = ExitGames.Client.Photon.Hashtable;
using UnityEngine.Animations;
using UnityEngine.SceneManagement;


public class PlayerController : MonoBehaviour
{


    #region Vars
    #region Inspector Reference Vars
    [SerializeField] GameObject cameraHolder;
    [SerializeField] public float mouseSenstivity, speed, jumpForce, smoothTime;
    [SerializeField] GameObject itemHolder;
    [SerializeField] GameObject weaponPivot;
    [SerializeField] GameObject Helmet, Body;
    [SerializeField] GameObject playerModel;
    [SerializeField] Camera cam;
    #endregion

    #region Location and Rotation Vars
    private float verticalLookRotation;
    bool grounded;
    Vector3 smoothMoveVelocity;
    Vector3 moveAmount;

    Vector3 moveDir, jumpDir;

    #endregion

    #region Player Vars
    Rigidbody rb;
    Hashtable customProperties = new Hashtable();
    Animator Animation;
    #endregion

    #region Health Vars
    public const float maxHealth = 45f;
    public float currentHealth = maxHealth;
    private int healthRechargeWait = 10;
    private int healthRechargePerSecond = 9;
    private bool isDead = false;
    #endregion
    #endregion

    public float horizontalMovement;
    public float verticalMovement;
    private float distToGround = 0.2f;

    public float maxSpeed = 20;
    public float attackDamage = 10;
    private bool attacking = false;
    private bool attackSound = true;

    private Animator animator;

    public Collider attackZoneCollider;


    public AudioClip audioClipC;
    public AudioClip audioClipW;
    public AudioClip audioClipM;
    public AudioClip audioClipBearDeath;
    public AudioClip audioClipBearAttack1;
    public AudioClip audioClipBearAttack2;
    private AudioSource audioSource;

    // Start is called before the first frame update
    void Start()
    {
        rb = gameObject.GetComponent<Rigidbody>();
        //distToGround = gameObject.GetComponent<BoxCollider>().bounds.extents.y;
        animator = gameObject.GetComponent<Animator>();

        audioSource = GetComponent<AudioSource>();
    }

    // Is called when bear collides with another object
    void OnTriggerEnter (Collider other)
    {
        if (other.CompareTag("Cocaine"))
        {
            audioSource.clip = audioClipC;
            audioSource.Play();
        }
        if (other.CompareTag("Weed"))
        {
            audioSource.clip = audioClipW;
            audioSource.Play();
        }
        if (other.CompareTag("Meth"))
        {
            audioSource.clip = audioClipM;
            audioSource.Play();
        }
    }

    /// <summary>
    /// Update method called continously based on frame rate of user to handle local inputs
    /// </summary>
    private void Update()
    {
        if (!isDead)
        {
            // This will detect forward and backward movement
            verticalMovement = Input.GetAxis("Vertical");
            if(!attacking && verticalMovement < 0)
            {
                animator.SetBool("WalkForward", false);
                animator.SetBool("WalkBackward", true);
            }
            else if(!attacking && verticalMovement > 0)
            {
                animator.SetBool("WalkForward", true);
                animator.SetBool("WalkBackward", false);
            }
            else
            {
                animator.SetBool("WalkForward", false);
                animator.SetBool("WalkBackward", false);
            }
            // This will detect sideways movement
            horizontalMovement = Input.GetAxis("Horizontal");
            //

            //Make sure that the character only animates the idle animation while paused
            //Animation.SetFloat("InputX", 0);
            //Animation.SetFloat("InputZ", 0);

            

            //Debug.Log(Input.GetKeyDown(KeyCode.Space));
            if (Input.GetKeyDown(KeyCode.Space))
            {
                Debug.Log(transform.up * jumpForce);
                jumpDir = transform.up * jumpForce;
                animator.SetBool("Jump", true);
            }
            else
            {
                animator.SetBool("Jump", false);
            }

            moveDir = transform.forward * verticalMovement + transform.right * horizontalMovement;
            //moveDir.Normalize();
        }

        //kill player controller if they don't have health
        if (currentHealth <= 0)
        {
            Die();
        }

        if (transform.position.y < -5f)
        {

            gameObject.transform.position = new Vector3(rb.position.x, 1, rb.position.z);
        }
    }

    /// <summary>
    /// Method is called at a fixed rate instead of being tied to framerate like update() to move the character model around the game
    /// </summary>
    private void FixedUpdate()
    {
        if (!isDead)
        {
            Look();
            if (IsGrounded())
            {
                Move();
                Jump();
            }
            else
            {
                Debug.Log("NotGrouned");
            }
            StartCoroutine(Attack());
        }
    }

    #region Movement
    /// <summary>
    /// Method which takes mouse inputs and converts that into camera movement in the game
    /// </summary>
    private void Look()
    {
        transform.Rotate(Vector3.up * Input.GetAxisRaw("Mouse X") * mouseSenstivity);

        //note the minus sign can be changed to a plus sign to invert mouse movement
        verticalLookRotation -= Input.GetAxisRaw("Mouse Y") * mouseSenstivity;
        verticalLookRotation = Mathf.Clamp(verticalLookRotation, -60f, 58f);

        //cameraHolder.transform.localEulerAngles = Vector3.left * verticalLookRotation;
    }

    /// <summary>
    /// Method which takes keyboard inputs and stores that into a movement amount var
    /// </summary>
    private void Move()
    {
        rb.AddForce(moveDir * speed, ForceMode.Impulse);
        rb.velocity = Vector3.ClampMagnitude(rb.velocity, maxSpeed);

        moveDir = new Vector3(0, 0, 0);
        //rb.AddForce(Vector3.SmoothDamp(moveAmount, moveDir * speed, ref smoothMoveVelocity, smoothTime));

        //Sprint Code
        //moveAmount = Vector3.SmoothDamp(moveAmount, moveDir * (Input.GetKey(KeyCode.LeftShift) ? sprintSpeed : walkSpeed), ref smoothMoveVelocity, smoothTime);
        //moveAmount = Vector3.SmoothDamp(moveAmount, moveDir * speed, ref smoothMoveVelocity, smoothTime);

        //Tell the animator which direction the character is moving in
        //Animation.SetFloat("InputX", moveAmount.x);
        //Animation.SetFloat("InputZ", moveAmount.z);

    }

    /// <summary>
    /// Method which allows character to jump if they are on the ground
    /// </summary>
    private void Jump()
    {
        //Debug.Log(jumpDir);
        rb.AddForce(jumpDir);//, ForceMode.Force);
        
        jumpDir = new Vector3(0, 0, 0);
    }

    private bool IsGrounded() {
        RaycastHit hit;
        return Physics.Raycast(transform.position, Vector3.down, out hit, distToGround);
    }

    private IEnumerator Attack()
    {
        if (!attacking && Input.GetMouseButtonDown(0))
        {
            attacking = true;
            Debug.Log("Attacking");
            animator.Play("Attack1", 0, 0.0f);
            if (attackSound)
            {
                audioSource.clip = audioClipBearAttack1;
            }
            else
                audioSource.clip = audioClipBearAttack2;
            audioSource.Play();
            attackSound = !attackSound;
            attackZoneCollider.enabled = true;
            Invoke("DisableAttackZone", .01f);
            yield return new WaitForSeconds(1f);
            attacking = false;
        }
    }

    public void Damage(float damage)
    {
        currentHealth -= damage;
    }

    public void Die()
    {
        if(!isDead)
        {
            animator.Play("Death", 0, 0.0f);
            audioSource.clip = audioClipBearDeath;
            audioSource.Play();
            maxSpeed = 0;
            isDead = true;
            Invoke("GameOver", 5f);
        }
    }

    private void GameOver()
    {
        SceneManager.LoadScene("GameOverScreen");
    }

    private void DisableAttackZone()
    {
        attackZoneCollider.enabled = false;
    }

    private void OnCollisionEnter(Collision collision)
    {
        if(collision.gameObject.tag == "Terrain")
        {
            grounded = true;
        }
    }
    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.tag == "Terrain")
        {
            grounded = false;
        }
    }
    #endregion
}