from pydantic import BaseModel
from typing import Optional, Any
from pydantic import Field

class FileMeta(BaseModel):
    name: str
    size: int = 0
    type: str = ""
    url: Optional[str] = None
    key: Optional[str] = None


class CompanyPayload(BaseModel):
    companyName: str = ""
    headquarters: str = ""
    yearsInOperation: str = ""
    completedProjects: str = ""
    keyMarkets: list[str] = Field(default_factory=list)
    companyWebsite: str = ""
    partnerships: str = ""
    unitsSold: str = ""
    numberOfInvestors: str = ""
    repeatBuyers: str = ""
    buyerTypes: list[str] = Field(default_factory=list)
    repName: str = ""
    repPersonalEmail: str = ""
    repOfficialEmail: str = ""
    repYearsActive: str = ""
    repDesignation: str = ""
    registrationCertificate: Optional[FileMeta] = None
    projectPortfolio: Optional[FileMeta] = None
    financialStatements: Optional[FileMeta] = None


class ProjectPayload(BaseModel):
    projectName: str = ""
    country: str = ""
    city: str = ""
    microLocation: str = ""
    projectType: str = ""
    projectStage: str = ""
    distanceToAirport: str = ""
    distanceToBusinessDistrict: str = ""
    publicTransportAccess: str = ""
    nearbyInfrastructure: str = ""
    areaType: str = ""
    metroStationName: str = ""
    metroDistanceKm: str = ""
    metroTravelMins: str = ""
    metroMode: str = ""
    railwayStationName: str = ""
    railwayDistanceKm: str = ""
    railwayTravelMins: str = ""
    airportName: str = ""
    airportDistanceKm: str = ""
    airportTravelMins: str = ""
    busHubName: str = ""
    busHubDistanceKm: str = ""
    busHubTravelMins: str = ""
    lastMileOptions: list[str] = Field(default_factory=list)
    peakHourCBD: str = ""
    currency: str = "USD"
    minTicketSize: str = ""
    maxTicketSize: str = ""
    pricePositioning: str = ""
    expectedAnnualReturns: str = ""
    rentalYieldEstimate: str = ""
    foreignInvestmentAllowed: str = ""
    ownershipStructure: str = ""
    goldenVisa: bool = False
    taxConsiderations: str = ""
    legalStructureNotes: str = ""
    expectedCompletionDate: str = ""
    totalUnits: str = ""
    unitsAvailable: str = ""
    unitTypes: list[dict[str, Any]] = Field(default_factory=list)
    developerTrackRecord: str = ""
    propertyDescription: str = ""
    propertyTags: list[str] = Field(default_factory=list)
    projectAddress: str = ""
    googleMapLink: str = ""
    totalFloors: str = ""
    unitTypology: list[str] = Field(default_factory=list)
    projectImages: list[FileMeta] = Field(default_factory=list)
    floorPlans: Optional[FileMeta] = None
    brochure: Optional[FileMeta] = None


class UploadEnvelope(BaseModel):
    companyDocuments: Optional[dict[str, Optional[FileMeta]]] = None
    agreement: Optional[dict[str, Optional[FileMeta]]] = None
    projectAssets: Optional[dict[str, Any]] = None


class PresignRequest(BaseModel):
    file_name: str
    content_type: str = "application/octet-stream"
    category: str


class ProfileSubmitRequest(BaseModel):
    company: CompanyPayload
    uploads: UploadEnvelope


class ProjectSubmitRequest(BaseModel):
    project_id: Optional[str] = None
    project: ProjectPayload
    uploads: UploadEnvelope

