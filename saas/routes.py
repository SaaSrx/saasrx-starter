class ROUTES:
    """
    Define URL routes for the application.
    Attributes:
        INDEX (str): Root path '/'
        API (str): API endpoint '/api'
        DASHBOARD (str): Dashboard page '/dashboard'
        DOWNLOAD (str): Download endpoint '/download'
        SIGNIN (str): Sign in page '/signin'
    Classes:
        AUTH: Authentication related routes
            Attributes:
                VERIFY (str): Authentication verification endpoint '/auth/verify'
        PAYMENT: Payment related routes
            Attributes:
                SUCCESS (str): Payment success callback '/payment/success'
    """

    INDEX = "/"

    API = "/api"

    #
    class AUTH:
        VERIFY = "/auth/verify"

    # dashboard = "/dashboard"
    DASHBOARD = "/dashboard"
    DOWNLOAD = "/download"

    class PAYMENT:
        SUCCESS = "/payment/success"

    SIGNIN = "/signin"
